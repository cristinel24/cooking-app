import os
import httpx
from constants import ErrorCodes
from schemas import PasswordHashRequestResponse


async def request_password_hash(password: str) -> PasswordHashRequestResponse:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{os.getenv('HASHER_API_URL', 'http://localhost:2020')}/{password}"
            response = await client.get(url=request_url)
            parsed_response = PasswordHashRequestResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise Exception(ErrorCodes.PASSWORD_HASH_REQUEST_FAILED.value)
