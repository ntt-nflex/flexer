import json
import os
import unittest

from flexer import CmpClient
from flexer.config import CONFIG_FILE, DEFAULT_CONFIG_YAML
from flexer.context import FlexerContext
from flexer.runner import Flexer
from flexer.utils import (
    load_config,
    lookup_credentials,
    read_yaml_file,
)

import main


class BaseConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.getenv("CONFIG_YAML", DEFAULT_CONFIG_YAML)
        cls.account = read_yaml_file(path)
        cls.account["credentials"] = (
            lookup_credentials(cls.account.get("credentials_keys"))
        )

        cls.runner = Flexer()
        cfg = load_config(cfg_file=CONFIG_FILE)["regions"]["default"]
        client = CmpClient(url=cfg["cmp_url"],
                           auth=(cfg['cmp_api_key'], cfg['cmp_api_secret']))
        cls.context = FlexerContext(cmp_client=client)

    def setUp(self):
        # TODO: See if we need extra parameters in the event
        self.event = {
            "credentials": self.account["credentials"],
        }

    def test_get_resources(self):
        result = self.runner.run(handler="main.get_resources",
                                 event=self.event,
                                 context=self.context)
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
                                 context=self.context)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertTrue(value["ok"])

    def test_validate_bad_credentials(self):
        self.event["credentials"] = {}

        result = self.runner.run(handler="main.validate_credentials",
                                 event=self.event,
                                 context=self.context)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertFalse(value["ok"])

    @unittest.skipIf(not hasattr(main, "get_metrics"),
                     "get_metrics not defined")
    def test_get_metrics(self):
        result = self.runner.run(handler="main.get_metrics",
                                 event=self.event,
                                 context=self.context)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        metrics = value["metrics"]
        self.assertIsNotNone(metrics)
        self.assertGreater(len(metrics), 0, 'No metrics found')

        expected_metrics = self.account['expected_metrics']
        for name in expected_metrics:
            count = len(filter(lambda r: r["metric"] == name, metrics))
            self.assertGreater(count, 0,
                               'No metric points for "%s" found' % name)
