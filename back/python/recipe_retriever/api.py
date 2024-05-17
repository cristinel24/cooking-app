import httpx
from constants import *
from exceptions import *


async def request_user_card(user_id: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=f"{USER_MICROSERVICE_URL}/user/{user_id}/card")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as http_exc:
        status_code = http_exc.response.status_code
        if status_code == 404:
            raise UserRetrieverException(status_code, ErrorCodes.USER_NOT_FOUND)
        else:
            raise UserRetrieverException(status_code, ErrorCodes.FAILED_TO_GET_USER_CARD)
    except Exception:
        raise UserRetrieverException(500, ErrorCodes.FAILED_TO_GET_USER_CARD)
