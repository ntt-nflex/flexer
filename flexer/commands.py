import getpass
import json

from flexer.config import CONFIG_FILE, DEFAULT_CMP_URL
from flexer.context import FlexerContext
from flexer.runner import Flexer


def config():
    url_prompt = 'CMP URL (default is "%s"): ' % DEFAULT_CMP_URL
    user_prompt = 'CMP API Key: '
    pass_prompt = 'CMP API Secret: '

    url = raw_input(url_prompt)
    key = raw_input(user_prompt)
    secret = getpass.getpass(pass_prompt)
    config = {
        'cmp_url': url or DEFAULT_CMP_URL,
        'cmp_api_key': key,
        'cmp_api_secret': secret,
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


def run(handler, event, cmp_client):
    event = json.loads(event)
    handler = "main.%s" % handler
    context = FlexerContext(cmp_client=cmp_client)
    runner = Flexer()
    return runner.run(event=event, context=context, handler=handler)
