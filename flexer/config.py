import os

CONFIG_FILE = os.path.expanduser('~/.flexer.json')
DEFAULT_CMP_URL = 'https://portal.ntt.eu/cmp/basic/api'


class Config(object):
    CMP_URL = os.getenv('CMP_URL', 'http://localhost/cmp/api')
    CMP_USERNAME = os.getenv('CMP_USERNAME', 'user')
    CMP_PASSWORD = os.getenv('CMP_PASSWORD', 'pass')
    NFLEX_CODEDIR = os.getenv('NFLEX_CODEDIR', '/sandbox')


class TestingConfig(Config):
    NFLEX_CODEDIR = '/tmp'
