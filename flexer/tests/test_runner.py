import json
import pytest
import mock
import sys
import unittest

from flexer.runner import Flexer
from flexer.context import FlexerContext

PYVERSION = "%s.%s" % (sys.version_info.major, sys.version_info.minor)

exc_message = {
    "nonexisting_module": {
        "2.7": "No module named not_here",
        "3.3": "No module named 'not_here'",
        "3.4": "No module named 'not_here'",
        "3.5": "No module named 'not_here'",
        "3.6": "No module named 'not_here'",
    },
    "nonexisting_handler": {
        "2.7": "'module' object has no attribute 'not_found'",
        "3.3": "'module' object has no attribute 'not_found'",
        "3.4": "'module' object has no attribute 'not_found'",
        "3.5": "module 'module_okay' has no attribute 'not_found'",
        "3.6": "module 'module_okay' has no attribute 'not_found'",
    },
    "invalid_handler": {
        "2.7": "need more than 1 value to unpack",
        "3.3": "need more than 1 value to unpack",
        "3.4": "need more than 1 value to unpack",
        "3.5": "not enough values to unpack (expected 2, got 1)",
        "3.6": "not enough values to unpack (expected 2, got 1)",
    },
    "import_error": {
        "2.7": 'No module named this_module_does_not_exist',
        "3.3": "No module named 'this_module_does_not_exist'",
        "3.4": "No module named 'this_module_does_not_exist'",
        "3.5": "No module named 'this_module_does_not_exist'",
        "3.6": "No module named 'this_module_does_not_exist'",
    },
    "module_level_exception": {
        "2.7": "need more than 1 value to unpack",
        "3.3": "need more than 1 value to unpack",
        "3.4": "need more than 1 value to unpack",
        "3.5": "not enough values to unpack (expected 2, got 1)",
        "3.6": "not enough values to unpack (expected 2, got 1)",
    },
    "handler_exception": {
        "2.7": "need more than 1 value to unpack",
        "3.3": "need more than 1 value to unpack",
        "3.4": "need more than 1 value to unpack",
        "3.5": "not enough values to unpack (expected 2, got 1)",
        "3.6": "not enough values to unpack (expected 2, got 1)",
    },
}

exc_type = {
    "import_error": {
        "2.7": 'ImportError',
        "3.3": 'ImportError',
        "3.4": 'ImportError',
        "3.5": 'ImportError',
        "3.6": 'ModuleNotFoundError',
    }
}


class TestFlexer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.runner = Flexer()

    def test_run_with_no_handler(self):
        """If run is called without a handler, an exception should be raised"""
        handler = ''
        expected = {
            'exc_message': 'Handler is required',
            'exc_type': 'Exception',
            'stack_trace': '',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertDictEqual(expected, actual['error'])

    def test_run_with_nonexisting_module(self):
        """If run is called with a non-existing module, an exception
        should be raised
        """
        handler = 'not_here.test'
        expected = {
            'exc_message': (
                'Failed to import module "not_here": %s'
                % exc_message["nonexisting_module"][PYVERSION]
            ),
            'exc_type': 'ImportError',
            'stack_trace': '',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertDictEqual(expected, actual['error'])

    def test_run_with_nonexisting_handler(self):
        """If run is called with a valid module, but non-existing handler,
        an exception should be raised
        """
        handler = 'module_okay.not_found'
        expected = {
            'exc_message': (
                'Handler "not_found" not found in "module_okay": %s'
                % exc_message["nonexisting_handler"][PYVERSION]
            ),
            'exc_type': 'AttributeError',
            'stack_trace': '',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertDictEqual(expected, actual['error'])

    def test_run_with_builtin_module(self):
        """If a built-in module is passed as a handler to run, an exception
        should be raised

        To get the list of all modules that are compiled into this Python
        interpreter, do: print sys.builtin_module_names

        sys happens to be one of these modules
        """
        handler = 'sys.exit'
        expected = {
            'exc_message': (
                'Built-in module "sys" cannot be a handler module'
            ),
            'exc_type': 'Exception',
            'stack_trace': '',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertDictEqual(expected, actual['error'])

    def test_run_with_invalid_handler(self):
        """If run is called with an invalid handler, i.e passing only a module
        or a method, an exception should be raised
        """
        handler = 'test'
        expected = {
            'exc_message': (
                'Invalid format for handler "test": %s'
                % exc_message["invalid_handler"][PYVERSION]
            ),
            'exc_type': 'ValueError',
            'stack_trace': '',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertDictEqual(expected, actual['error'])

    def test_run_with_import_error(self):
        """Make sure ImportErrors are handled during module imports.
        If there is an ImportError raised, the exception should store the
        stack trace.
        """
        handler = 'module_with_import_error.test'
        exc_m = exc_message["import_error"][PYVERSION]
        exc_t = exc_type["import_error"][PYVERSION]
        expected = {
            'exc_message': (
                'Failed to import module "module_with_import_error": %s'
                % exc_m
            ),
            'exc_type': exc_t,
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('%s: %s' % (exc_t, exc_m), error['stack_trace'])

    def test_run_with_syntax_error(self):
        """Make sure SyntaxErrors are handled during module imports.
        If there is a SyntaxError raised, the exception should store the
        stack trace.
        """
        handler = 'module_with_syntax_error.test'
        expected = {
            'exc_message': (
                'Syntax error in module "module_with_syntax_error": '
                'invalid syntax (module_with_syntax_error.py, line 2)'
            ),
            'exc_type': 'SyntaxError',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('this is a syntax error', error['stack_trace'])

    def test_run_with_module_level_exception(self):
        """Make sure all exceptions are handled during module imports.
        If there is an Exception raised, a stack trace should be available
        in the exception as well
        """
        handler = 'module_with_exception.test'
        exc_m = exc_message["module_level_exception"][PYVERSION]
        expected = {
            'exc_message': (
                'Failed to initialise "module_with_exception": %s' % exc_m
            ),
            'exc_type': 'ValueError',
        }
        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('ValueError: %s' % exc_m, error['stack_trace'])

    def test_run_with_no_stdout_logs(self):
        """Test the simplest possible use-case: run a method with no side
        effects and make sure the result is stored
        """
        handler = 'module_okay.test_with_no_logs'
        expected = {
            'value': 42,
            'error': None,
            'logs': '',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertDictEqual(expected, actual)

    def test_run_with_stdout_logs(self):
        """Run a method with side effects and make sure that the result is
        stored and the stdout/stderr are captured
        """
        handler = 'module_okay.test_with_logs'
        expected = {
            'value': 42,
            'error': None,
            'logs': 'This goes to stdout\n',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertDictEqual(expected, actual)

    def test_run_with_handler_exception(self):
        """Run a method that raises an Exception. Store the error details as
        a result from the execution and make sure that the stdout/stderr are
        still captured. The stack trace is expected to be part of the logs.
        """
        handler = 'module_okay.test_with_exception'
        exc_m = exc_message["handler_exception"][PYVERSION]
        expected = {
            'exc_message': exc_m,
            'exc_type': 'ValueError',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertIn('Before the exception\nTraceback', actual['logs'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('ValueError: %s' % exc_m, error['stack_trace'])

    @pytest.mark.skip(reason="We don't have to worry about memory locally")
    def test_run_with_memory_error(self):
        """Make sure MemoryErrors are handled when running the code.
        """
        handler = 'module_with_memory_error.test'
        expected = {
            'exc_message': '',
            'exc_type': 'MemoryError',
        }
        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertIn('Starting Up\n', actual['logs'])
        error = actual['error']

        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('MemoryError', error['stack_trace'])

    def test_run_with_invalid_db_secret(self):
        """Run a method that tries to use an invalid secret for an Nflex DB
        """
        handler = 'module_with_db.test'
        expected = {
            'exc_message': 'The mydb secret is not a valid MongoDB connection string',  # noqa
            'exc_type': 'Exception',
        }
        context = FlexerContext()
        secrets = [
            "test",
            "mongodb://",
            "mongodb://a",
            "mongodb://a:b",
            "mongodb://a:b@",
            "mongodb://a:b@c",
            "mongodb://a:b@c/",
        ]
        for s in secrets:
            context.secrets = {"_nflexdb_mydb": s}
            result = self.runner.run(event={}, context=context, handler=handler)

            actual = json.loads(result)
            self.assertEqual(None, actual['value'])
            error = actual['error']

            self.assertEqual(expected['exc_message'], error['exc_message'])
            self.assertEqual(expected['exc_type'], error['exc_type'])
            self.assertIn('Exception', error['stack_trace'])

    def test_run_with_valid_db_secret(self):
        """Run a method that tries to use a valid secret for an Nflex DB
        """
        handler = 'module_with_db.test'
        context = FlexerContext()
        context.secrets = {"_nflexdb_mydb": "mongodb://a:b@c/mydb"}
        with mock.patch(
                'MongoClient',
                return_value=mock.MagicMock()):
            result = self.runner.run(event={}, context=context, handler=handler)

            actual = json.loads(result)
            self.assertTrue('error' in actual)
            self.assertTrue('value' in actual)
            self.assertEqual(None, actual['error'])
            self.assertTrue('result' in actual['value'])

    def test_run_with_validation_error(self):
        """Run a method that returns data with validation errors and make sure
        its being caught and stored in the logs
        """
        handler = 'module_with_validation_error.test'
        expected = {
            'value': None,
            'error': {
                'exc_message': '["10 is not of type \'string\' in result.foo"]',
                'exc_type': 'ValidationError'
            },
            'logs': '["10 is not of type \'string\' in result.foo"]',
        }
        schema = {
            'patternProperties': {
                '.*': {'type': 'string'},
            }
        }

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema',
                return_value=schema):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertDictEqual(expected, actual)

    def test_validate_metrics_ok(self):
        """Run a method that returns metric data and check validation is ok
        """
        handler = 'module_with_metrics.test_ok'
        expected = {
            u'value': {u'metrics': [{
                u'metric': u'cpu-usage',
                u'value': 99,
                u'unit': u'percent',
                u'time': u'2017-01-12T18:30:42.034751Z',
                u'resource_id': u'1237ab91-08eb-4164-8e68-67699c29cd4c'}
                ]},
            u'error': None,
            u'logs': u'Running test script\n',
        }

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_metrics.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertDictEqual(expected, actual)

    def test_validate_metrics_error(self):
        """Run a method that returns metric data and check validation is ok
        """
        handler = 'module_with_metrics.test_invalid'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_metrics.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('value' in actual)
        self.assertIsNone(actual['value'])
        self.assertTrue('exc_type' in actual['error'])
        self.assertTrue('exc_message' in actual['error'])
        self.assertEqual(u'ValidationError', actual['error']['exc_type'])
        self.assertTrue("\'time\' is a required property"
                        in actual['error']['exc_message'])

    def test_validate_logs_ok(self):
        """Run a method that returns log data and check validation is ok
        """
        handler = 'module_with_logs.test_ok'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_logs.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('value' in actual)
        self.assertTrue('logs' in actual['value'])
        self.assertEqual(1, len(actual['value']['logs']))
        self.assertEqual(None, actual['error'])

    def test_validate_logs_error(self):
        """Run a method that returns log data and check validation is ok
        """
        handler = 'module_with_logs.test_invalid'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_logs.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('exc_type' in actual['error'])
        self.assertTrue('exc_message' in actual['error'])
        self.assertEqual(u'ValidationError', actual['error']['exc_type'])
        self.assertTrue("\'time\' is a required property"
                        in actual['error']['exc_message'])

    def test_validate_logs_invalid_severity_error(self):
        """
        Run a method that returns log data and check validation is NG
        with invalid severity
        """
        handler = 'module_with_logs.test_invalid_severity_value'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_logs.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('exc_type' in actual['error'])
        self.assertTrue('exc_message' in actual['error'])
        self.assertEqual(u'ValidationError', actual['error']['exc_type'])
        self.assertIn('HIGH', actual['error']['exc_message'])
        self.assertIn('is not one of', actual['error']['exc_message'])

    def test_validate_status_ok(self):
        """Run a method that returns status data and check validation is ok
        """
        handler = 'module_with_status.test_ok'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_status.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('value' in actual)
        self.assertEqual(None, actual['error'])
        self.assertTrue('status' in actual['value'])
        self.assertEqual(3, len(actual['value']['status']))

    def test_validate_status_missing_level_error(self):
        """Run a method that returns status data and check validation is NG
        with missing level
        """
        handler = 'module_with_status.test_missing_level'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_status.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('exc_type' in actual['error'])
        self.assertTrue('exc_message' in actual['error'])
        self.assertEqual(u'ValidationError', actual['error']['exc_type'])
        self.assertTrue("\'level\' is a required property"
                        in actual['error']['exc_message'])

    def test_validate_status_missing_time_error(self):
        """Run a method that returns status data and check validation is NG
        with missing time
        """
        handler = 'module_with_status.test_missing_time'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_status.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('exc_type' in actual['error'])
        self.assertTrue('exc_message' in actual['error'])
        self.assertEqual(u'ValidationError', actual['error']['exc_type'])
        self.assertTrue("\'time\' is a required property"
                        in actual['error']['exc_message'])

    def test_validate_status_invalid_status_error(self):
        """Run a method that returns status data and check validation is NG
        with invalid status
        """
        handler = 'module_with_status.test_invalid_level'

        with mock.patch(
                'flexer.runner.Flexer._get_validation_schema_file',
                return_value='get_status.json'):
            result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertTrue('error' in actual)
        self.assertTrue('exc_type' in actual['error'])
        self.assertTrue('exc_message' in actual['error'])
        self.assertEqual(u'ValidationError', actual['error']['exc_type'])
        self.assertIn("3 is not one of", actual['error']['exc_message'])

    def test_validate_spend_schema(self):
        """
        Run a few methods to test spend json schema validation
        """

        handlers = [
            'module_spend_validator.good_spend1',
            'module_spend_validator.good_spend2',
            'module_spend_validator.good_spend3',
        ]
        bad_handlers = [
            'module_spend_validator.bad_spend1',
            'module_spend_validator.bad_spend2',
            'module_spend_validator.bad_spend3',
        ]

        to_patch = 'flexer.runner.Flexer._get_validation_schema_file'
        with mock.patch(to_patch, return_value='get_spend.json'):
            for handler in handlers:
                result = self.runner.run(event={}, context=None, handler=handler)
                load = json.loads(result)
                self.assertFalse(load['error'])

            for handler in bad_handlers:
                result = self.runner.run(event={}, context=None, handler=handler)
                load = json.loads(result)
                self.assertTrue(load['error'])
