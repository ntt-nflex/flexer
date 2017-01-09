import json
import unittest
import pytest
import mock

from flexer.runner import Flexer


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
                'Failed to import module "not_here": No module named not_here'
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
                'Handler "not_found" not found in "module_okay": '
                '\'module\' object has no attribute \'not_found\''
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
                'Invalid format for handler "test": '
                'need more than 1 value to unpack'
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
        expected = {
            'exc_message': (
                'Failed to import module "module_with_import_error": '
                'No module named this_module_does_not_exist'
            ),
            'exc_type': 'ImportError',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn(
            'ImportError: No module named this_module_does_not_exist\n',
            error['stack_trace']
        )

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
        expected = {
            'exc_message': (
                'Failed to initialise "module_with_exception": '
                'need more than 1 value to unpack'
            ),
            'exc_type': 'ValueError',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('ValueError: need more than 1 value to unpack',
                      error['stack_trace'])

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
        expected = {
            'exc_message': (
                'need more than 1 value to unpack'
            ),
            'exc_type': 'ValueError',
        }

        result = self.runner.run(event={}, context=None, handler=handler)

        actual = json.loads(result)
        self.assertEqual(None, actual['value'])
        self.assertIn('Before the exception\nTraceback', actual['logs'])
        error = actual['error']
        self.assertEqual(expected['exc_message'], error['exc_message'])
        self.assertEqual(expected['exc_type'], error['exc_type'])
        self.assertIn('ValueError: need more than 1 value to unpack',
                      error['stack_trace'])

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

    def test_run_with_validation_error(self):
        """Run a method that returns data with validation errors and make sure
        its being caught and stored in the logs
        """
        handler = 'module_with_validation_error.test'
        expected = {
            'value': {'foo': 10},
            'error': {
                'exc_message': '["10 is not of type \'string\' in [\'foo\']"]',
                'exc_type': 'ValidationError'
            },
            'logs': '["10 is not of type \'string\' in [\'foo\']"]',
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
