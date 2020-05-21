from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.logging import Logger
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.util.retry import Retry
import requests


tracer = Tracer()
logger = Logger()


class AddressTransaction:
    @tracer.capture_method
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        retries: int = 3,
        timeout: float = 2.00,
    ):
        self.host = host
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.session.auth = (username, password)
        self.timeout = timeout
        self.username = username
        self.password = password
        self.url = f"https://{self.host}/address_transactions"
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=0.1,
            status_forcelist=(429, 500, 502, 504),
            method_whitelist=("POST",),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)

    @tracer.capture_method
    def request(self, payload: dict):
        url = payload.get("url", self.url)
        if url.endswith("/confirm") or url.endswith("/close"):
            resp = self.session.post(url, timeout=self.timeout,)
        else:
            resp = self.session.post(url, json=payload, timeout=self.timeout,)
        resp.raise_for_status()
        return resp.json()


@tracer.capture_method
def get_address(address_lookup: AddressTransaction, user_data: dict):
    address_data = {}
    confirmation_url = {}
    retry_url = {}
    data = {}

    logger.info({"messsage": f"requesting {user_data.get('phone')}"})
    resp = address_lookup.request(user_data)
    if resp:
        address_data = resp["address"] if resp.get("address") else {}
        confirm_link = resp["confirmation_link"]
        close_link = resp["close_link"]

        data = {
            "FirstName": address_data.get("first_name"),
            "LastName": address_data.get("last_name"),
            "AddressL1": address_data.get("line1"),
            "AddressL2": address_data.get("line2"),
            "City": address_data.get("city"),
            "State": address_data.get("state"),
            "Zip": address_data.get("zip"),
            "CloseUrl": f"https://{address_lookup.host}{close_link}",
            "ConfirmationUrl": f"https://{address_lookup.host}{confirm_link}"
            if confirm_link
            else None,
        }

    return data


@tracer.capture_method
def confirm_address(address_lookup: AddressTransaction, url: str):
    payload = {"url": url}
    return address_lookup.request(payload)


@tracer.capture_method
def close_address_tx(address_lookup: AddressTransaction, url: str):
    payload = {"url": url}
    return address_lookup.request(payload)
