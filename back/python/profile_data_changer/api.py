import httpx
import json
from fastapi import status
from constants import ALLERGEN_MANAGER_API_URL, ErrorCodes, INC_ALLERGENS, DEC_ALLERGENS
from exception import ProfileDataChangerException


async def request_inc_allergens(allergens: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_API_URL}{INC_ALLERGENS}"
        payload = json.dumps({"allergens": allergens})
        response = await client.post(url, content=payload)
        if response.status_code != status.HTTP_200_OK:
            error_code = response.json()["errorCode"] if "errorCode" in response.json() else ErrorCodes.SERVER_ERROR.value
            raise ProfileDataChangerException(response.status_code, error_code=error_code)


async def request_dec_allergens(allergens: list[str]) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_API_URL}{DEC_ALLERGENS}"
        payload = json.dumps({"allergens": allergens})
        response = await client.post(url, content=payload)
        if response.status_code != status.HTTP_200_OK:
            error_code = response.json()["errorCode"] if "errorCode" in response.json() else ErrorCodes.SERVER_ERROR.value
            raise ProfileDataChangerException(response.status_code, error_code=error_code)
