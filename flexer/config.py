import os
import sys
import flexer

CONFIG_FILE = os.path.expanduser('~/.flexer.yaml')
DEFAULT_CMP_URL = 'https://sandbox.cmp.nflex.io/cmp/basic/api'
DEFAULT_CONFIG_YAML = os.path.join(os.getcwd(), "config.yaml")


class Config(object):
    CMP_URL = os.getenv('CMP_URL', 'http://localhost/cmp/api')
    CMP_REGION = os.getenv('CMP_REGION', '')
    CMP_PLATFORM = os.getenv('CMP_PLATFORM', '')
    CMP_USERNAME = os.getenv('CMP_USERNAME', '')
    CMP_PASSWORD = os.getenv('CMP_PASSWORD', '')
    CMP_ACCESS_TOKEN = os.getenv('CMP_ACCESS_TOKEN', '')
    FLEXER_VERSION = os.getenv('FLEXER_VERSION', '')
    NFLEX_CODEDIR = os.getenv('NFLEX_CODEDIR', '/sandbox')
    MODULE_ID = os.getenv('NFLEX_MODULE_ID')
    DB_KEY_PREFIX = '_nflexdb_'

    USER_AGENT = (
        "flexer/%s "
        "flexer_py%d%d/%s "
        "(module=%s platform=%s region=%s)"
    ) % (
        flexer.__version__,
        sys.version_info.major,
        sys.version_info.minor,
        FLEXER_VERSION or "unknown",
        MODULE_ID or "unknown",
        CMP_PLATFORM or "unknown",
        CMP_REGION or "unknown",
    )


class TestingConfig(Config):
    NFLEX_CODEDIR = '/tmp'
