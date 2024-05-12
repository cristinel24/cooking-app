from pprint import pprint

import httpx
from fastapi import status

from constants import ID_GENERATOR_API_URL, ID_GENERATOR_ROUTE, ErrorCodes
from exception import ImageStorageException


async def get_id() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=ID_GENERATOR_API_URL + ID_GENERATOR_ROUTE)
        if response.json().get("id") is None:
            if response.json().get("errorCode") is None:
                raise ImageStorageException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                raise ImageStorageException(int(response.json()["errorCode"]), status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response.json()["id"]
