import json
import os
import unittest
import yaml

from flexer.context import FlexerContext
from flexer.runner import Flexer


DEFAULT_ACCOUNT_YAML = os.path.join(os.getcwd(), "account.yaml")


class BaseConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.getenv("TEST_ACCOUNT_YAML", DEFAULT_ACCOUNT_YAML)
        with open(path) as f:
            cls.account = yaml.load(f)
            if "credentials" not in cls.account:
                cls.account["credentials"] = {}

            for key in cls.account.get("credentials_keys", []):
                cls.account["credentials"][key] = os.getenv(key.upper())

        cls.runner = Flexer()

    def setUp(self):
        # TODO: See if we need extra parameters in the event
        self.retries = self.account.get("test_retries", 1)
        self.event = {
            "credentials": self.account["credentials"],
        }

    def test_get_resources(self):
        result = self.runner.run(handler="main.get_resources",
                                    event=self.event)
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
                                 event=self.event)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertTrue(value["ok"])

    def test_validate_bad_credentials(self):
        self.event["credentials"] = {}

        result = self.runner.run(handler="main.validate_credentials",
                                 event=self.event)
        result = json.loads(result)

        self.assertIsNone(result["error"])
        value = result["value"]
        self.assertIsNotNone(value)
        self.assertFalse(value["ok"])

    def test_get_metrics(self):
        result = self.runner.run(handler="main.get_metrics",
                                    event=self.event)
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
