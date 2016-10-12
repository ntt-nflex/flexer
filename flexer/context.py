from datetime import datetime
import logging

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
        if cmp_client is None:
            self.api_url = Config.CMP_URL
            self.api_auth = (Config.CMP_USERNAME, Config.CMP_PASSWORD)
            self.api = CmpClient(self.api_url, self.api_auth)
        else:
            self.api_url = cmp_client._url
            self.api_auth = cmp_client._auth
            self.api = cmp_client

    def log(self, message, severity="info"):
        """Log a message to CMP."""
        try:
            r = self.api.post("/logs", [
                {
                    "message": message,
                    "severity": severity.upper(),
                    "service": "nflex.runner",
                    "timestamp": datetime.utcnow().strftime(
                        '%Y-%m-%dT%H:%M:%S.%fZ'
                    ),
                }
            ])

        except Exception as err:
            logger.error("Error sending logs to CMP: %s", err)

        if r.status_code != 200:
            logger.error("Error sending logs to CMP: %s", r.text)

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

        except Exception as err:
            logger.error("Error sending logs to CMP: %s", err)

        if r.status_code != 200:
            logger.error("Error sending logs to CMP: %s", r.text)

    def set_response_header(self, key, value):
        """Set a response header"""
        self.response_headers[key] = value
