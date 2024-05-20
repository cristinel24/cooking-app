import httpx

from fastapi import status

from exceptions import LoginException
from schemas import HasherResponse, TokenResponse
from constants import Errors, HASHER_API_URL, TOKEN_GENERATOR_API_URL


async def request_hash(target: str, alg_name: str, salt: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{HASHER_API_URL}/{alg_name}/{target}?salt={salt}"
            response = await client.get(url=formated_url)
            parsed_response = HasherResponse.model_validate(response.json(), strict=True)
            return parsed_response  # object of type HasherResponse
    except Exception:
        raise LoginException(Errors.HASH_ERROR, status.HTTP_503_SERVICE_UNAVAILABLE)


async def request_token(user_id: str, token_type: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{TOKEN_GENERATOR_API_URL}/{user_id}/{token_type}"
            response = await client.get(url=formated_url)
            parsed_response = TokenResponse.model_validate(response.json(), strict=True)
            return parsed_response  # object of type TokenResponse
    except Exception:
        raise LoginException(Errors.TOKEN_ERROR, status.HTTP_503_SERVICE_UNAVAILABLE)
