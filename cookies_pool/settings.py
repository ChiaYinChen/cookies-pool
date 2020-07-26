"""General settings."""
import logging
import logging.config
import os
from distutils.util import strtobool
from os.path import abspath, dirname, join

# path settings
PROJ_ROOT = dirname(dirname(abspath(__file__)))
DRIVER_PATH = join(PROJ_ROOT, 'src', 'geckodriver')
LOG_FILE_PATH = join(PROJ_ROOT, 'cookies_pool', 'logging.conf')

# logging setting
logging.config.fileConfig(LOG_FILE_PATH)

# redis settings
REDIS_SETTINGS = {
    'host': os.environ.get('REDIS_HOST', 'redis'),
    'port': os.environ.get('REDIS_PORT', 6379)
}

# crawl settings
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'  # noqa: E501

# process settings
GENERATOR_PROCESS_ENABLED = bool(strtobool(os.environ.get('GENERATOR_PROCESS_ENABLED', 'TRUE')))  # noqa: E501
TESTER_PROCESS_ENABLED = bool(strtobool(os.environ.get('TESTER_PROCESS_ENABLED', 'TRUE')))  # noqa: E501
GENERATOR_MAP = ('facebook', 'instagram',)
TESTER_MAP = ('facebook', 'instagram',)
