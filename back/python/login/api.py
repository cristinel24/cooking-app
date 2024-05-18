import os
import httpx

from exceptions import LoginException
from schemas import HasherResponse, TokenResponse
from constants import Errors

HASHER_URL = os.getenv("HASHER_URL", "http://localhost:8202")
TOKEN_GEN_URL = os.getenv("TOKEN_GEN_URL", "http://localhost:8256")


async def request_hash(target: str, alg_name: str, salt: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{HASHER_URL}/{alg_name}/{target}?salt={salt}"
            response = await client.get(url=formated_url)
            parsed_response = HasherResponse.model_validate(response.json(), strict=True)
            return parsed_response  # object of type HasherResponse
    except Exception:
        raise LoginException(Errors.HASH_ERROR, "hash error")


async def request_token(user_id: str, token_type: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{TOKEN_GEN_URL}/{user_id}/{token_type}"
            response = await client.get(url=formated_url)
            parsed_response = TokenResponse.model_validate(response.json(), strict=True)
            return parsed_response  # object of type TokenResponse
    except Exception:
        raise LoginException(Errors.TOKEN_ERROR, "token error")
