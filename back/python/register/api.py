import httpx
from fastapi import status

import constants
import exceptions
import schemas


async def hash_password(password: str):
    url = f"{constants.HASHER_API_URL}{constants.HASHER_ROUTE}.format(target={password})"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url)
            parsed_response = schemas.HasherResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except exceptions.RegisterException as e:
        raise exceptions.RegisterException(error_code=constants.ErrorCodes.PASSWORD_HASHING_FAILED,
                                           status_code=e.status_code)


async def generate_token(user_id: str, token_type: str) -> str:
    url = (f"{constants.TOKEN_GENERATOR_API_URL}"
           f"{constants.TOKEN_GENERATOR_ROUTE}.format(user_id={user_id}, token_type={token_type})")

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.RegisterException(error_code=constants.ErrorCodes.TOKEN_GENERATION_FAILED,
                                               status_code=response.status_code)
        return response.json()["user_id"]


async def generate_user_id() -> str:
    async with httpx.AsyncClient() as client:
        url = f"{constants.ID_GENERATOR_API_URL}{constants.ID_GENERATOR_ROUTE}"
        response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.RegisterException(error_code=constants.ErrorCodes.ID_GENERATION_FAILED,
                                               status_code=response.status_code)
        return response.json()["user_id"]


async def send_verification_email(email: str, token: str):
    url = f"{constants.EMAIL_SYSTEM_API_URL}{constants.EMAIL_SYSTEM_ROUTE}"

    params = {
        "email": email,
        "token": token
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.RegisterException(error_code=constants.ErrorCodes.EMAIL_SENDING_FAILED,
                                               status_code=response.status_code)
        return response.json()["user_id"]


async def destroy_user(user_id: str):
    url = f"{constants.USER_DESTROYER_API_URL}{constants.DESTROY_USER_ROUTE}.format(user_id={user_id})"

    async with httpx.AsyncClient() as client:
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.RegisterException(error_code=constants.ErrorCodes.USER_DATA_VALIDATION_ERROR,
                                               status_code=response.status_code)
        return response.json()["user_id"]


async def destroy_token(token: str):
    async with httpx.AsyncClient() as client:
        url = f"{constants.TOKEN_DESTROYER_API_URL}{constants.TOKEN_DESTROYER_ROUTE}.format(token={token})"
        response = await client.delete(url)
        if response.status_code != status.HTTP_200_OK:
            raise exceptions.RegisterException(error_code=constants.ErrorCodes.USER_DATA_VALIDATION_ERROR,
                                               status_code=response.status_code)
        return response.json()["user_id"]
