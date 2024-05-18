import httpx
from constants import *
from exceptions import CredentialChangeRequesterException
from fastapi import status
from schemas import *


async def request_token(user_id: str, token_type: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=TOKEN_GENERATOR_API_URL + f"/{user_id}{token_type}")
        if response.status_code != status.HTTP_200_OK:
            raise CredentialChangeRequesterException(response.status_code, response.json()["errorCode"])
        return response.json()["token"]


async def send_email(request: ChangeRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=EMAIL_SYSTEM_API_URL + f"/request_change", json=request.dict())
        if response.status_code != status.HTTP_200_OK:
            raise CredentialChangeRequesterException(response.status_code, response.json()["errorCode"])
