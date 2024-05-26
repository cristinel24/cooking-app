from aiohttp import ClientSession, ClientTimeout, ClientError, ClientResponseError

from schemas import AuthorCardData
from utils import singleton, init_logger, async_retry
from constants import ID_GENERATOR_API_URL, USER_RETRIEVER_API_URL
from exceptions import InternalError, ExternalError

REQUEST_TIMEOUT: int = 5
ERROR_FIELD: str = 'errorCode'
request_errors = (ClientError, ClientResponseError, TimeoutError)


@singleton
class ExternalDataProvider:

    def __init__(self):
        self.logger = init_logger("[ExternalDataProvider]")
        self.timeout = ClientTimeout(total=REQUEST_TIMEOUT)

    @async_retry(request_errors)
    async def generate_id(self) -> str:
        async with ClientSession(timeout=self.timeout) as session:
            async with session.get(ID_GENERATOR_API_URL) as response:
                self.logger.info(f'Request {ID_GENERATOR_API_URL}')
                response = await response.json()

        if isinstance(response, dict) and response.get(ERROR_FIELD):
            raise ExternalError()
        return response["id"]

    @async_retry(request_errors)
    async def get_user(self, user_id: str | None) -> AuthorCardData:
        if user_id is None:
            raise InternalError()

        async with ClientSession(timeout=self.timeout) as session:
            url = f'{USER_RETRIEVER_API_URL}/{user_id}/card'
            async with session.get(url) as response:
                self.logger.info(f'Request {url}')
                response = await response.json()

        if isinstance(response, dict) and response.get(ERROR_FIELD):
            raise ExternalError()

        return AuthorCardData(**response)
