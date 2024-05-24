import httpx
from constants import *
from exception import VerifierException
from fastapi import status


async def request_is_token_valid(token_value: str) -> str:
    async with httpx.AsyncClient() as client:
        url = f"{TOKEN_VALIDATOR_API_URL}{VERIFY_TOKEN_ROUTE.format(token_type=EMAIL_CHANGE_TOKEN, token=token_value)}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise VerifierException(status_code=response.status_code, error_code=response.json()["errorCode"])
        return response.json()["userId"]


async def request_destroy_token(token_value: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{TOKEN_DESTROYER_API_URL}{DESTROY_TOKEN_ROUTE.format(token=token_value)}"
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            raise VerifierException(status_code=response.status_code, error_code=response.json()["errorCode"])
