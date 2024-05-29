import httpx
import json
from fastapi import status
from constants import ALLERGEN_MANAGER_API_URL, ErrorCodes, POST_ALLERGENS
from exception import ProfileDataChangerException


async def post_allergens(allergens: list[str], action: int) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{ALLERGEN_MANAGER_API_URL}{POST_ALLERGENS}?action={action}"
        payload = json.dumps({"allergens": allergens})
        response = await client.post(url, content=payload)
        if response.status_code != status.HTTP_200_OK:
            error_code = response.json()["errorCode"] if "errorCode" in response.json() else ErrorCodes.SERVER_ERROR.value
            raise ProfileDataChangerException(response.status_code, error_code=error_code)
