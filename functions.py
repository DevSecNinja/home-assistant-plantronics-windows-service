import logging

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util.retry import Retry


def get_http_result(url):
    """Sends a GET request with unlimited retries and a backoff factor."""

    requestsSession = Session()
    retries = Retry(
        total=None, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
    )
    requestsSession.mount("http://", HTTPAdapter(max_retries=retries))
    try:
        r = requestsSession.get(url)
        return r
    except ConnectionError:
        logging.warn(f"Request to URL failed: {url}")
        pass
