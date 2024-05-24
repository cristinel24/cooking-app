import json
import httpx
from constants import (ErrorCodes, TOKEN_GENERATOR_API_URL, EMAIL_SYSTEM_API_URL,  TOKEN_VALIDATOR_API_URL,
                       TOKEN_DESTROYER_API_URL, DESIRED_EMAIL_CHANGE_TOKEN_TYPE)
from schemas import TokenGeneratorRequestResponse, TokenValidatorRequestResponse


async def request_token_generation(user_id: str, token_type: str) -> TokenGeneratorRequestResponse:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{TOKEN_GENERATOR_API_URL}/{user_id}/{token_type}"
            response = await client.get(url=request_url)
            parsed_response = TokenGeneratorRequestResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise Exception(ErrorCodes.TOKEN_GENERATOR_REQUEST_FAILED.value)


async def request_email_verification(email: str, token: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{EMAIL_SYSTEM_API_URL}/verify-account"
            response = await client.post(url=request_url, content=json.dumps({"email": email, "token": token}))
            if response.json() is not None:
                raise Exception()
    except Exception:
        raise Exception(ErrorCodes.EMAIL_SYSTEM_REQUEST_FAILED.value)


async def request_token_validation(token: str) -> TokenValidatorRequestResponse:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{TOKEN_VALIDATOR_API_URL}/{DESIRED_EMAIL_CHANGE_TOKEN_TYPE}/{token}"
            response = await client.get(url=request_url)
            parsed_response = TokenValidatorRequestResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise Exception(ErrorCodes.TOKEN_VALIDATOR_REQUEST_FAILED.value)


async def request_token_destroy(user_id: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{TOKEN_DESTROYER_API_URL}/{user_id}/all"
            response = await client.delete(url=request_url)
            if response.json() is not None:
                raise Exception()
    except Exception:
        raise Exception(ErrorCodes.TOKEN_DESTROYER_REQUEST_FAILED.value)
