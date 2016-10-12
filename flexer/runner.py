# -*- coding: utf-8 -*-

import StringIO
import datetime
import imp
import json
import logging
import sys
import traceback

from flexer.context import FlexerContext

logger = logging.getLogger('flexer.runner')


def dthandler(obj):
    if isinstance(obj, (datetime.datetime, datetime.time)):
        return obj.isoformat()


class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


class FlexerException(Exception):
    def __init__(self, exc_message, exc_type, stack_trace=''):
        self.exc_message = str(exc_message)
        self.exc_type = exc_type.__name__
        self.stack_trace = stack_trace

    def to_dict(self):
        return {
            'exc_message': self.exc_message,
            'exc_type': self.exc_type,
            'stack_trace': self.stack_trace,
        }


def FlexerResult(value=None, logs='', error=None, headers=None):
    result = {
        "value": value,
        "logs": logs,
        "error": error,
    }
    if headers:
        result['headers'] = headers

    try:
        return json.dumps(result, default=dthandler)

    except Exception as e:
        msg = ("An error occurred during JSON serialization of the result: %s"
               % e)
        exc = FlexerException(exc_message=msg, exc_type=type(e))
        result['value'] = None
        result['error'] = exc.to_dict()
        return json.dumps(result)


class Flexer(object):
    def __init__(self):
        self.modules = {}

    def run(self, event, context=None, handler=None):
        if context is None:
            context = FlexerContext()

        logger.info('Running handler "%s"', handler)
        try:
            module_name, func_name = self._parse_handler(handler)
            if module_name not in self.modules:
                self.modules[module_name] = self._import_module(module_name)

            func = self._get_handler_from_module(module_name, func_name)

        except FlexerException as e:
            return FlexerResult(value=None,
                                logs=e.stack_trace,
                                error=e.to_dict())

        value, error, stdout = None, None, ''
        headers = {}
        f = StringIO.StringIO()
        try:
            with RedirectStdStreams(stdout=f, stderr=f):
                try:
                    value = func(event, context)
                    headers = context.response_headers

                    # if a cmp object type is returned,
                    # encode result and add header
                    if hasattr(value, "cmp_response"):
                        headers['x-cmp-response'] = type(value).__name__
                        value = value.cmp_response()

                except:
                    del func
                    error = self._format_exception_info(sys.exc_info())

            stdout = f.getvalue()

        finally:
            f.close()
            logger.info('Handler completed "%s"', handler)

        if error:
            stdout += error['stack_trace']

        return FlexerResult(value=value,
                            logs=stdout,
                            error=error,
                            headers=headers)

    def _format_exception_info(self, exc_info):
        exc_type, value, tb = exc_info
        stack_trace = format_stack_trace(exc_info)
        return {
            'exc_message': str(value),
            'exc_type': exc_type.__name__,
            'stack_trace': stack_trace
        }

    def _parse_handler(self, handler):
        if not handler:
            raise FlexerException('Handler is required', Exception)

        try:
            module_name, func_name = handler.rsplit('.', 1)
            return module_name, func_name

        except ValueError as e:
            msg = 'Invalid format for handler "{}": {}'.format(handler, e)
            raise FlexerException(msg, type(e))

    def _get_handler_from_module(self, module_name, func_name):
        try:
            module = self.modules[module_name]
            return getattr(module, func_name)

        except AttributeError as e:
            msg = 'Handler "{}" not found in "{}": {}'.format(func_name,
                                                              module_name,
                                                              e)
            raise FlexerException(msg, type(e))

    def _import_module(self, module_name):
        logger.info('Importing module "%s"', module_name)
        file_ = None
        # Import the module
        try:
            file_, pathname, description = imp.find_module(module_name)

        except ImportError as e:
            msg = 'Failed to import module "{}": {}'.format(module_name, e)
            raise FlexerException(msg, type(e))

        # Do not allow using builtin modules as handlers
        _, _, module_type = description
        if file_ is None:
            if module_type == imp.C_BUILTIN:
                msg = ('Built-in module "{}" cannot be a handler module'
                       .format(module_name))
                raise FlexerException(msg, Exception)

        # Load the module
        try:
            module = imp.load_module(module_name, file_, pathname, description)

        except ImportError as e:
            msg = 'Failed to import module "{}": {}'.format(module_name, e)
            stack_trace = format_stack_trace(sys.exc_info())
            raise FlexerException(msg, type(e), stack_trace)

        except SyntaxError as e:
            stack_trace = (
                'File \"%s\", line %s\n\t%s' % (e.filename.split('/')[-1],
                                                e.lineno,
                                                e.text)
            )
            msg = 'Syntax error in module "{}": {}'.format(module_name, e)
            raise FlexerException(msg, type(e), stack_trace)

        except Exception as e:
            stack_trace = format_stack_trace(sys.exc_info())
            msg = 'Failed to initialise "{}": {}'.format(module_name, e)
            raise FlexerException(msg, type(e), stack_trace)

        finally:
            if file_ is not None:
                file_.close()

        return module


# utility methods
def format_stack_trace(exc_info):
    exc_type, value, tb = exc_info
    tb_details = traceback.extract_tb(tb)
    # remove the runner from the stack trace
    for i in range(len(tb_details)):
        filename = tb_details[i][0]  # filename of the module
        if "/runner.py" not in filename:
            tb_details = tb_details[i:]
            break

    return (
        'Traceback (most recent call last):\n' +
        ''.join(traceback.format_list(tb_details)) +
        ''.join(traceback.format_exception_only(exc_type, value))
    )
