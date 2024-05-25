import httpx
from constants import *
from exceptions import *
from fastapi import status


async def request_user_card(user_id: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=f"{USER_RETRIEVER_API_URL}/{user_id}/card")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as http_exc:
        status_code = http_exc.response.status_code
        if status_code == status.HTTP_404_NOT_FOUND:
            raise UserRetrieverException(status_code, ErrorCodes.USER_NOT_FOUND)
        else:
            raise UserRetrieverException(status_code, ErrorCodes.FAILED_TO_GET_USER_CARD)
    except Exception:
        raise UserRetrieverException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.FAILED_TO_GET_USER_CARD)
