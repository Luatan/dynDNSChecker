import requests
from logger import logger


class Ip:
    def __init__(self):
        self.current_ip = get_public_ip()

    def update(self) -> bool:
        public_ip = get_public_ip()
        if public_ip != self.current_ip:
            logger.info(f"Public ip address changed to: {public_ip}")
            self.current_ip = public_ip
            return True
        return False


def get_public_ip() -> str:
    response = requests.get("https://eth0.me")
    if response.status_code != 200:
        raise
    return str(response.content.decode(response.encoding)).strip()
