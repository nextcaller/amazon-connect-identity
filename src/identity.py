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
def get_address(address_lookup: AddressTransaction, payload: dict):
    return address_lookup.request(payload)


@tracer.capture_method
def finalize_tx(address_lookup: AddressTransaction, url: str):
    payload = {"url": url}
    return address_lookup.request(payload)
