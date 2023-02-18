import sys
import requests
import json

from constants import Constants
from http_methods import Method
from logger import logger


class Api:
    def __init__(self):
        self.api_key = Constants.API_KEY.value
        self.domain = Constants.DOMAIN.value
        self.hosts = self.__create_host_dict()
        self.zone_id = self.update_zone_identification()
        self.update_dns_identification()
        logger.info(f"[{Constants.PROVIDER.value}] Initial Data was fetched")

    def __request(self, url, method=Method.GET, data=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.request(method.name, url, headers=headers, data=data)
        if response.status_code != 200:
            logger.error(response)
            raise Exception(f"Failed to contact API of {Constants.PROVIDER.value}")
        json_response = json.loads(response.content)
        if json_response['success'] is False:
            error = json_response['errors']['message']
            logger.error(f"Got Error from API {error}")
            raise Exception(error)
        return json_response

    def update_zone_identification(self) -> str:
        logger.info(f"[{Constants.PROVIDER.value}] Fetching Zone info")
        response = self.__request("https://api.cloudflare.com/client/v4/zones")
        for zone in response['result']:
            if zone['name'] == self.domain:
                return zone['id']
        if self.zone_id is None:
            logger.error("No Zone found")
            sys.exit(1)

    def __create_host_dict(self) -> dict:
        records = Constants.HOSTS.value
        hosts = {}
        for record in records:
            if record == "@":
                hosts[self.domain] = ""
                continue
            if not str(record).endswith(self.domain):
                hosts[f"{record}.{self.domain}"] = ""
            else:
                hosts[record] = ""
        return hosts

    def update_dns_identification(self) -> None:
        logger.info(f"[{Constants.PROVIDER.value}] Fetching DNS-Records")
        response = self.__request(f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records")
        for dns in response['result']:
            if dns['name'] in self.hosts:
                self.hosts[dns['name']] = dns['id']

    def create_record(self, name, ip) -> None:
        logger.info(f"Creating {name} for {ip}")
        response = self.__request(
            url=f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records",
            method=Method.POST,
            data=json.dumps({
                "name": name,
                "type": "A",
                "content": ip,
                "ttl": 1
            }))
        self.hosts[response['result']['name']] = response['result']['id']
        logger.info(f"[{Constants.PROVIDER.value}] DNS-Record for {name} successfully created!")

    def update_record(self, record_name: str, target_ip: str) -> None:
        if self.hosts[record_name] == '':
            logger.info(f"Record does not exist yet. Creating instead")
            self.create_record(record_name, target_ip)
            return

        self.__request(
            url=f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{self.hosts[record_name]}",
            method=Method.PATCH,
            data=json.dumps({"content": target_ip}))
        logger.info(f"Updated {record_name} to {target_ip}")

    def check_record(self, record_name: str) -> str:
        if self.hosts[record_name] == '':
            return ""
        response = self.__request(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{self.hosts[record_name]}")
        return response['result']['content']
