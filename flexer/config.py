import os

CONFIG_FILE = os.path.expanduser('~/.flexer.yaml')
DEFAULT_CMP_URL = 'https://sandbox.cmp.nflex.io/cmp/basic/api'
DEFAULT_CONFIG_YAML = os.path.join(os.getcwd(), "config.yaml")


class Config(object):
    CMP_URL = os.getenv('CMP_URL', 'http://localhost/cmp/api')
    CMP_USERNAME = os.getenv('CMP_USERNAME', '')
    CMP_PASSWORD = os.getenv('CMP_PASSWORD', '')
    CMP_ACCESS_TOKEN = os.getenv('CMP_ACCESS_TOKEN', '')
    NFLEX_CODEDIR = os.getenv('NFLEX_CODEDIR', '/sandbox')
    MODULE_ID = os.getenv('NFLEX_MODULE_ID')
    DB_KEY_PREFIX = '_nflexdb_'


class TestingConfig(Config):
    NFLEX_CODEDIR = '/tmp'
