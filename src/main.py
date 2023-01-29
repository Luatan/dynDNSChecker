import sys
import time

import signal
from ipManagement import IpCheck
from cloudflareApi import Api
from constants import Constants
from logger import logger


def signal_handler(sig, frame):
    logger.warning("Shutting down")
    sys.exit(0)


def call_api(api, current_ip):
    for record in api.hosts.keys():
        record_ip = api.check_record(record)
        if record_ip != current_ip:
            api.update_record(record, current_ip)


def main():
    if not Constants.API_KEY.value:
        logger.error(
            f"No API Key was entered. Make sure you use the environment variable API_KEY to set your {Constants.PROVIDER.value} key")
        sys.exit(1)
    if not Constants.DOMAIN.value:
        logger.error(
            f"No Domain was entered. Use the environment variable DOMAIN to set the domain, which should be checked")
        sys.exit(1)
    api = Api()
    ip_check = IpCheck()

    # make sure the current ip is set as record
    call_api(api, ip_check.current_ip)

    while True:
        logger.info(f"Waiting {Constants.INTERVAL.value / 60} minutes for next IP Check")
        time.sleep(Constants.INTERVAL.value)
        if not ip_check.ip_changed():
            continue
        call_api(api, ip_check.current_ip)


if __name__ == '__main__':
    # register interrupt handler
    signal.signal(signal.SIGINT, signal_handler)

    main()
