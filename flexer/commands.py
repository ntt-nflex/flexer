import getpass
import json

from flexer.config import CONFIG_FILE, DEFAULT_CMP_URL
from flexer.context import FlexerContext
from flexer.runner import Flexer


def config():
    url_prompt = 'CMP URL (default is "%s"): ' % DEFAULT_CMP_URL
    user_prompt = 'CMP Username: '
    pass_prompt = 'CMP Password: '

    url = raw_input(url_prompt)
    username = raw_input(user_prompt)
    passw = getpass.getpass(pass_prompt)
    config = {
        'cmp_url': url or DEFAULT_CMP_URL,
        'cmp_username': username,
        'cmp_password': passw,
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)


def run(handler, event, cmp_client):
    event = json.loads(event)
    handler = "main.%s" % handler
    context = FlexerContext(cmp_client=cmp_client)
    runner = Flexer()
    return runner.run(event=event, context=context, handler=handler)
