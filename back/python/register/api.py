import httpx
from fastapi import status

from constants import *
from exception import RegisterException


async def request_generate_user_id() -> str:
    async with httpx.AsyncClient() as client:
        url = f"{ID_GENERATOR_API_URL}{ID_GENERATOR_ROUTE}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise RegisterException(status_code=response.status_code, error_code=ErrorCodes.ID_GENERATION_FAILED.value)
        return response.json()["id"]


async def request_hash(password: str) -> dict[str, str]:
    async with httpx.AsyncClient() as client:
        url = f"{HASHER_API_URL}{HASHER_ROUTE.format(target=password)}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise RegisterException(status_code=response.status_code, error_code=ErrorCodes.PASSWORD_HASHING_FAILED.value)
        return response.json()


async def request_generate_token(user_id: str, token_type: str) -> str:
    async with httpx.AsyncClient() as client:
        url = f"{TOKEN_GENERATOR_API_URL}{TOKEN_GENERATOR_ROUTE.format(user_id=user_id, token_type=token_type)}"
        print(url)
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise RegisterException(status_code=response.status_code, error_code=ErrorCodes.TOKEN_GENERATION_FAILED.value)
        return response.json()["value"]


async def request_send_verification_email(email: str, token: str) -> None:
    async with httpx.AsyncClient() as client:
        url = EMAIL_SYSTEM_API_URL + EMAIL_SYSTEM_ROUTE
        payload = {
            "email": email,
            "token": token
        }
        response = await client.post(url, json=payload)
        if response.status_code != status.HTTP_200_OK:
            raise RegisterException(status_code=response.status_code, error_code=ErrorCodes.EMAIL_SENDING_FAILED.value)


async def request_destroy_user(user_id: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{USER_DESTROYER_API_URL}{DESTROY_USER_ROUTE.format(user_id=user_id)}"
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            raise RegisterException(status_code=response.status_code, error_code=ErrorCodes.USER_DESTROY_FAILED.value)


async def request_destroy_token(token: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{TOKEN_DESTROYER_API_URL}{TOKEN_DESTROYER_ROUTE.format(token=token)}"
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            raise RegisterException(status_code=response.status_code, error_code=ErrorCodes.TOKEN_DESTROY_FAILED.value)
