import sys
import requests
import json

from constants import Constants
from httpmethods import HTTPMethods
from ipManagement import get_public_ip
from logger import logger


class Api:
    def __init__(self):
        self.api_key = Constants.API_KEY.value
        self.domain = Constants.DOMAIN.value
        self.hosts = self.create_host_dict()
        self.zone_id = self.update_zone_identification()
        self.update_dns_identification()
        logger.info(f"[{Constants.PROVIDER.value}] Initial Data was fetched")

    def _request_api(self, url, method=HTTPMethods.GET, data=None):
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
        response = self._request_api("https://api.cloudflare.com/client/v4/zones")
        for zone in response['result']:
            if zone['name'] == self.domain:
                return zone['id']
        if self.zone_id is None:
            logger.error("No Zone found")
            sys.exit(1)

    def create_host_dict(self) -> dict:
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
        response = self._request_api(f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records")
        for dns in response['result']:
            if dns['name'] in self.hosts:
                self.hosts[dns['name']] = dns['id']

    def create_record(self, name, ip) -> None:
        logger.info(f"Creating {name} for {ip}")
        data = {
            "name": name,
            "type": "A",
            "content": ip,
            "ttl": 1
        }
        response = self._request_api(
            url=f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records",
            method=HTTPMethods.POST,
            data=json.dumps(data))
        self.hosts[response['result']['name']] = response['result']['id']
        logger.info(f"[{Constants.PROVIDER.value}] DNS-Record for {name} successfully created!")

    def update_record(self, record_name: str, target_ip: str) -> None:
        logger.info(f"Updating {record_name} to {target_ip}")
        data = {
            "content": target_ip
        }
        self._request_api(
            url=f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{self.hosts[record_name]}",
            method=HTTPMethods.PATCH,
            data=json.dumps(data))

    def check_record(self, record_name: str) -> str:
        if self.hosts[record_name] == '':
            self.create_record(record_name, get_public_ip())
        response = self._request_api(
            f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records/{self.hosts[record_name]}")
        return response['result']['content']