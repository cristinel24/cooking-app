import httpx
import json
from fastapi import status
from constants import ALLERGEN_MANAGER_API_URL
from exception import ProfileDataChangerException


async def request_add_or_remove_allergens(allergens: list[str], method: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_API_URL}{method}"
        print(url)
        payload = json.dumps(allergens)
        response = await client.post(url, content=payload)
        if response.status_code != status.HTTP_200_OK:
            raise ProfileDataChangerException(response.status_code, error_code=response.json()["errorCode"])
