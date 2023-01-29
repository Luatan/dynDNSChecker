import requests
from logger import logger


class IpCheck:
    def __init__(self):
        self.current_ip = get_public_ip()

    def ip_changed(self) -> bool:
        public_ip = get_public_ip()
        if public_ip == self.current_ip:
            logger.info("No Changes to IP")
            return False
        logger.info(f"Public ip address changed to: {public_ip}")
        self.current_ip = public_ip
        return True


def get_public_ip() -> str:
    response = requests.get("https://eth0.me")
    if response.status_code != 200:
        raise
    return str(response.content.decode(response.encoding)).strip()
