from datetime import datetime
import logging
import copy

from flexer import CmpClient
from flexer.config import Config

logger = logging.getLogger('flexer.context')


class FlexerContext(object):
    """The FlexerContext object provides context to the nflex module
    during it's execution.
    """

    def __init__(self, cmp_client=None):
        """Construct a new FlexerContext object."""
        self.response_headers = {}
        self.config = {}
        self.secrets = {}
        self.state = None
        self.module_id = Config.MODULE_ID

        if cmp_client is None:
            auth = (Config.CMP_USERNAME, Config.CMP_PASSWORD)
            self.api = CmpClient(url=Config.CMP_URL,
                                 auth=auth,
                                 access_token=Config.CMP_ACCESS_TOKEN)
        else:
            self.api = cmp_client

        self.api_url = self.api.api_url
        self.api_auth = self.api.api_auth
        self.api_token = self.api.api_token

    def log(self, message, severity="info"):
        """Log a message to CMP."""
        try:
            payload = {
                "message": message,
                "severity": severity.upper(),
                "service": "nflex.flexer",
                "timestamp": datetime.utcnow().strftime(
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                ),
            }
            if self.module_id:
                payload["resource_id"] = "nflex-module-%s" % self.module_id

            r = self.api.post("/logs", [payload])

        except Exception as err:
            print("Error sending logs to CMP: %s" % err)

        if r.status_code != 200:
            print("Error sending logs to CMP: %s" % r.text)

    def mail(self,
             user=None,
             group=None,
             matter='nflex-email-default',
             medium='email',
             subject=None,
             message=None,
             params=None):
        """Send an email through CMP."""
        if params is None:
            params = {}

        url = ''
        if user:
            url = '/notifications/send/%s' % user
        elif group:
            url = '/notifications/groups/%s/send' % group
        else:
            url = '/notifications/send'

        # function keyword helpers for subject and message
        # (used in default template)
        if subject:
            params['subject'] = subject

        if message:
            params['message'] = message

        try:
            r = self.api.post(url, {
                'matter': matter,
                'medium': medium,
                'params': params,
            })

            if r.status_code != 200:
                logger.error("Error sending logs to CMP: %s", r.text)

        except Exception as err:
            logger.error("Error sending logs to CMP: %s", err)

    def set_response_header(self, key, value):
        """Set a response header"""
        self.response_headers[key] = value


class FlexerLocalState:

    def __init__(self):
        self.state = {}

    def get(self, key):
        return self.state.get(key)

    def set(self, key, value):
        self.state[key] = value

    def get_all(self):
        return copy.copy(self.state)

    def set_multi(self, updates):
        self.state.update(updates)


class FlexerRemoteState:

    def __init__(self, context):
        self.api = context.api
        self.module_id = Config.MODULE_ID

    def get(self, key):
        return self.get_all().get(key)

    def get_all(self):
        r = self.api.get("/modules/%s/state" % self.module_id)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception("Failed to read state: %s" % r.text)

    def set(self, key, value):
        self.set_multi({key: value})

    def set_multi(self, updates):
        r = self.api.patch("/modules/%s/state" % self.module_id, updates)
        if r.status_code != 200:
            raise Exception("Failed to update state: %s" % r.text)
