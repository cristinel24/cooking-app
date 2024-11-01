import httpx
from fastapi import status
from constants import *
from exception import RegisterException


async def request_generate_user_id() -> str:
    async with httpx.AsyncClient() as client:
        url = f"{ID_GENERATOR_API_URL}{ID_GENERATOR_ROUTE}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            handle_request_exception(response)
        return response.json()["id"]


async def request_hash(password: str) -> dict[str, str]:
    async with httpx.AsyncClient() as client:
        url = f"{HASHER_API_URL}{HASHER_ROUTE.format(target=password)}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            handle_request_exception(response)
        return response.json()


async def request_generate_token(user_id: str, token_type: str) -> str:
    async with httpx.AsyncClient() as client:
        url = f"{TOKEN_GENERATOR_API_URL}{TOKEN_GENERATOR_ROUTE.format(user_id=user_id, token_type=token_type)}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            handle_request_exception(response)
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
            handle_request_exception(response)


async def request_destroy_user(user_id: str) -> None:
    async with httpx.AsyncClient() as client:
        url = f"{USER_DESTROYER_API_URL}{DESTROY_USER_ROUTE.format(user_id=user_id)}"
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            handle_request_exception(response)


def handle_request_exception(response) -> None:
    response_json = response.json()
    if "errorCode" in response_json:
        error_code = response_json["errorCode"]
    else:
        error_code = ErrorCodes.SERVER_ERROR.value
    raise RegisterException(status_code=response.status_code, error_code=error_code)
