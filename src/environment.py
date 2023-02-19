import os
import sys
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


def handle_args():
    arg_var = sys.argv[1:]
    if len(arg_var) == 0:
        return ['@']
    return arg_var


class Constants(Enum):
    API_KEY = os.environ.get('API_KEY', None)
    DOMAIN = os.environ.get('DOMAIN', None)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    INTERVAL = int(os.environ.get('INTERVAL', 180))
    PROVIDER = "Cloudflare"
    HOSTS = handle_args()
