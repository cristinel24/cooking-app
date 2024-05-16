import httpx
from fastapi import status
from constants import ALLERGEN_MANAGER_URL, ErrorCodes
from exception import ProfileDataChangerException


async def request_add_allergen(allergen_name: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_URL}/allergen/{allergen_name}"
        response = await client.post(url)
        if response.status_code != status.HTTP_200_OK:
            raise ProfileDataChangerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.ADD_ALLERGEN_ERROR)


async def request_remove_allergen(allergen_name: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_URL}/allergen/{allergen_name}"
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            raise ProfileDataChangerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.REMOVE_ALLERGEN_ERROR)
