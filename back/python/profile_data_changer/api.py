import httpx
import json
from fastapi import status
from constants import ALLERGEN_MANAGER_API_URL, ErrorCodes, ADD_ALLERGENS, REMOVE_ALLERGENS
from exception import ProfileDataChangerException


async def request_add_allergens(allergens: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_API_URL}{ADD_ALLERGENS}"
        payload = json.dumps({"allergens": allergens})
        response = await client.post(url, content=payload)
        if response.status_code != status.HTTP_200_OK:
            error_code = response.json()["errorCode"] if "errorCode" in response.json() else ErrorCodes.SERVER_ERROR.value
            raise ProfileDataChangerException(response.status_code, error_code=error_code)


async def request_remove_allergens(allergens: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_API_URL}{REMOVE_ALLERGENS}"
        payload = json.dumps({"allergens": allergens})
        response = await client.post(url, content=payload)
        if response.status_code != status.HTTP_200_OK:
            error_code = response.json()["errorCode"] if "errorCode" in response.json() else ErrorCodes.SERVER_ERROR.value
            raise ProfileDataChangerException(response.status_code, error_code=error_code)
