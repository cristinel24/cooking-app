import requests
from utils import singleton, init_logger, retry
from constants import ID_GENERATOR_API_URL, USER_RETRIEVER_API_URL
from exceptions import InternalError

REQUEST_TIMEOUT: int = 5
request_errors = (requests.exceptions.RequestException, requests.exceptions.ConnectionError)


@singleton
class ExternalDataProvider:

    def __init__(self):
        self.logger = init_logger("[ExternalDataProvider]")

    @retry(request_errors)
    def generate_id(self) -> str:
        return requests.get(ID_GENERATOR_API_URL, timeout=REQUEST_TIMEOUT).json()

    @retry(request_errors)
    def get_user(self, user_id: str | None) -> str:
        if user_id is None:
            raise InternalError()
        return requests.get(f'{USER_RETRIEVER_API_URL}/{user_id}', timeout=REQUEST_TIMEOUT).json()
