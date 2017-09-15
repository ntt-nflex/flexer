import json
import os
import unittest

from flexer import CmpClient
from flexer.config import CONFIG_FILE, DEFAULT_CONFIG_YAML
from flexer.context import FlexerContext
from flexer.runner import Flexer
from flexer.utils import (
    load_config,
    lookup_values,
    read_yaml_file,
)

import main
import re


class BaseConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''The rule to evaluate number as boolean is inspired by C++11 implementation
        All numbers but 0 and True or true will be evaluated as True
        ''' # noqa
        cls.logging = re.search(r'^-?[1-9][0-9]*$|^[Tt]rue$',
                                os.getenv("LOG_TO_STDOUT", "False")) != None # noqa
        path = os.getenv("CONFIG_YAML", DEFAULT_CONFIG_YAML)
        cls.account = read_yaml_file(path)
        cls.account["credentials"] = (
            lookup_values(cls.account.get("credentials_keys"))
        )
        if "resources" in cls.account:
            cls.resource_data = cls.account.get("resources")
        else:
            cls.resource_data = [
                {
                    "resource": cls.account.get("resource", {}),
                    "expected_metrics": cls.account.get("expected_metrics"),
                    "expected_logs": cls.account.get("expected_logs"),
                }
            ]

        cls.runner = Flexer()
        cfg = load_config(cfg_file=CONFIG_FILE)["regions"]["default"]
        client = CmpClient(url=cfg["cmp_url"],
                           auth=(cfg['cmp_api_key'], cfg['cmp_api_secret']))
        cls.context = FlexerContext(cmp_client=client)
        secrets = (lookup_values(cls.account.get("secrets_keys")))
        cls.context.secrets = secrets

    def setUp(self):
        self.event = {
            "credentials": self.account["credentials"],
        }

    def fake_credentials(self):
        fake_credentials = {}
        for cred in self.event["credentials"].keys():
            fake_credentials[cred] = self.event["credentials"][cred] + '_fake'

        self.event["credentials"] = fake_credentials

    def test_get_resources(self):
        result = self.runner.run(handler="main.get_resources",
                                 event=self.event,
                                 context=self.context,
                                 debug=self.logging)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        resources = result["value"]
        self.assertIsNotNone(resources)
        self.assertGreater(len(resources), 0, 'No resources found')

        expected_resources = self.account['expected_resources']
        for rtype in expected_resources:
            count = len(filter(lambda r: r["type"] == rtype, resources))
            self.assertGreater(count, 0,
                               'No resources of type "%s" found' % rtype)

    def test_validate_credentials(self):
        result = self.runner.run(handler="main.validate_credentials",
                                 event=self.event,
                                 context=self.context,
                                 debug=self.logging)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertTrue(value["ok"])

    def test_validate_empty_credentials(self):
        # empty credentials
        self.event["credentials"] = {}

        result = self.runner.run(handler="main.validate_credentials",
                                 event=self.event,
                                 context=self.context,
                                 debug=self.logging)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertFalse(value["ok"])

    def test_validate_bad_credentials(self):
        self.fake_credentials()

        result = self.runner.run(handler="main.validate_credentials",
                                 event=self.event,
                                 context=self.context,
                                 debug=self.logging)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertFalse(value["ok"])

    def test_get_resources_when_bad_credentials(self):
        self.fake_credentials()

        result = self.runner.run(handler="main.get_resources",
                                 event=self.event,
                                 context=self.context,
                                 debug=self.logging)
        result = json.loads(result)

        error = result["error"]
        self.assertIsNotNone(error)
        self.assertEqual(error["exc_type"], 'AuthenticationException')
        self.assertIsNone(result["value"])

    @unittest.skipIf(not hasattr(main, "get_metrics"),
                     "get_metrics not defined")
    def test_get_metrics(self):
        for res in self.resource_data:
            self.event['resource'] = res['resource']
            self.event['resource_id'] = res['resource'].get('id')
            self.event['account_id'] = res['resource'].get('account_id')
            result = self.runner.run(handler="main.get_metrics",
                                     event=self.event,
                                     context=self.context,
                                     debug=self.logging)
            result = json.loads(result)

            self.assertIsNone(result["error"])
            value = result["value"]
            metrics = value["metrics"]
            self.assertIsNotNone(metrics)
            self.assertGreater(len(metrics), 0, 'No metrics found')

            expected_metrics = res['expected_metrics']
            for name in expected_metrics:
                self.assertTrue(
                    any(True for r in metrics if r["metric"] == name),
                    'No metric points for "%s" found' % name
                )

    @unittest.skipIf(not hasattr(main, "get_logs"),
                     "get_logs not defined")
    def test_get_logs(self):
        for res in self.resource_data:
            self.event['resource'] = res['resource']
            self.event['resource_id'] = res['resource'].get('id')
            self.event['account_id'] = res['resource'].get('account_id')
            result = self.runner.run(
                handler="main.get_logs",
                event=self.event,
                context=self.context,
                debug=self.logging,
            )
            result = json.loads(result)

            self.assertIsNone(result["error"])
            value = result["value"]
            logs = value["logs"]
            self.assertIsNotNone(logs)

            expected_logs = res['expected_logs']

            for severity in expected_logs:
                self.assertTrue(
                    any(True for log in logs
                        if log.get("severity", '') == severity),
                    'No log points for log with severity %s' % severity
                )
