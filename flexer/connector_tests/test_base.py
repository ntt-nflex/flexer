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
    client = None

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
        cls.skip_logs = cls.account.get('skip_logs', False)
        if "resources" in cls.account:
            cls.resource_data = cls.account.get("resources")
        else:
            cls.resource_data = [
                {
                    # config specific data used to set up the tests
                    "resource": cls.account.get("resource", {}),
                    "expected_metrics": cls.account.get("expected_metrics"),
                    "expected_logs": cls.account.get("expected_logs"),
                    "expected_status": cls.account.get("expected_status"),
                }
            ]

        cls.runner = Flexer()
        if not cls.client:
            cfg = load_config(cfg_file=CONFIG_FILE)["regions"]["default"]
            cls.client = CmpClient(
                url=cfg["cmp_url"],
                auth=(cfg['cmp_api_key'], cfg['cmp_api_secret'])
            )

        cls.context = FlexerContext(cmp_client=cls.client)
        secrets = (lookup_values(cls.account.get("secrets_keys")))
        cls.context.secrets = secrets

    def setUp(self):

        self.event = {
            # nflex scheduler base data
            "account_id": self.account.get("account_id"),
            "customer_id": self.account.get("customer_id"),
            "user_id": self.account.get("user_id"),
            "provider": self.account.get("provider"),
            "poll_interval": self.account.get("poll_interval"),
            "poll_type": self.account.get("poll_type"),
            "credentials": self.account["credentials"],
            "resource": self.account.get("resource", {})
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
                                 event_source="cmp-connector.resources",
                                 debug=self.logging)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        resources = result["value"]
        self.assertIsNotNone(resources)
        self.assertGreater(len(resources), 0, 'No resources found')

        expected_resources = self.account['expected_resources']
        for rtype in expected_resources:
            count = len(list(filter(lambda r: r["type"] == rtype, resources)))
            self.assertGreater(count, 0,
                               'No resources of type "%s" found' % rtype)

    def test_validate_credentials(self):
        result = self.runner.run(handler="main.validate_credentials",
                                 event=self.event,
                                 context=self.context,
                                 event_source="cmp-connector.credentials",
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
                                 event_source="cmp-connector.credentials",
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
                                 event_source="cmp-connector.credentials",
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
                                 event_source="cmp-connector.resources",
                                 debug=self.logging)
        result = json.loads(result)

        error = result["error"]
        self.assertIsNotNone(error)
        self.assertEqual(error["exc_type"], 'AuthenticationException')
        self.assertIsNone(result["value"])

    @staticmethod
    def _set_event(event, res):
        event['resource'] = res['resource']
        try:
            event['account_id'] = res['resource']['account_id']
            event['customer_id'] = res['resource']['customer_id']
            event['resource_id'] = res['resource']['id']
        except KeyError:
            # use the account id set at setUp
            pass
        return event

    @unittest.skipIf(not hasattr(main, "get_metrics"),
                     "get_metrics not defined")
    def test_get_metrics(self):
        counter = 0
        for res in self.resource_data:
            expected_metrics = res.get('expected_metrics')
            if expected_metrics is None:
                continue

            counter += 1
            event = BaseConnectorTest._set_event(self.event, res)
            result = self.runner.run(handler="main.get_metrics",
                                     event=event,
                                     context=self.context,
                                     event_source="cmp-connector.metrics",
                                     debug=self.logging)
            result = json.loads(result)

            self.assertIsNone(result["error"])
            value = result["value"]
            metrics = value["metrics"]
            self.assertIsNotNone(metrics)
            self.assertGreater(len(metrics), 0, 'No metrics found')

            for name in expected_metrics:
                self.assertTrue(
                    any(r["metric"] == name for r in metrics),
                    'No metric points for "%s" found' % name
                )
        self.assertNotEqual(counter, 0, "No expected_metrics found in config")

    @unittest.skipIf(not hasattr(main, "get_logs"),
                     "get_logs not defined")
    def test_get_logs(self):
        if self.skip_logs:
            self.skipTest("skip_logs flag raised")
        counter = 0
        for res in self.resource_data:
            expected_logs = res.get('expected_logs')
            if expected_logs is None:
                continue

            counter += 1
            event = BaseConnectorTest._set_event(self.event, res)
            result = self.runner.run(
                handler="main.get_logs",
                event=event,
                context=self.context,
                event_source="cmp-connector.logs",
                debug=self.logging,
            )
            result = json.loads(result)

            self.assertIsNone(result["error"])
            value = result["value"]
            logs = value["logs"]
            self.assertIsNotNone(logs)

            for severity in expected_logs:
                self.assertTrue(
                    any(log.get("severity", '') == severity for log in logs),
                    'No log points for log with severity %s' % severity
                )
        self.assertNotEqual(counter, 0, "No expected_logs found in config")

    @unittest.skipIf(not hasattr(main, "get_status"),
                     "get_status not defined")
    def test_get_status(self):
        counter = 0
        for res in self.resource_data:
            expected_status = res.get('expected_status')
            if expected_status is None:
                continue

            counter += 1
            event = BaseConnectorTest._set_event(self.event, res)
            result = self.runner.run(
                handler="main.get_status",
                event=event,
                context=self.context,
                event_source="cmp-connector.status",
                debug=self.logging,
            )
            result = json.loads(result)

            self.assertIsNone(result["error"])
            value = result["value"]
            status = value["status"]
            self.assertIsNotNone(status)

            for level in expected_status:
                self.assertTrue(
                    any(i.get("level", '') == level for i in status),
                    'No status points with level %s' % level
                )
        self.assertNotEqual(counter, 0, "No expected_status found in config")
