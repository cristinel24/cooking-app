import json

import httpx
from fastapi import status

from constants import MESSAGE_HISTORY_MANAGER_API_URL, ErrorCodes
from exceptions import AIException


async def get_message_history(user_id: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=MESSAGE_HISTORY_MANAGER_API_URL + f"/{user_id}/message-history?start=0&count=10",
            headers={
                "x-user-id": user_id,
            }
        )

        if response.status_code != status.HTTP_200_OK:
            raise AIException(
                error_code=int(response.json()["errorCode"]),
                status_code=response.status_code
            )

        return response.json()["history"]


async def add_message_to_history(user_id: str, message: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.put(
            url=MESSAGE_HISTORY_MANAGER_API_URL + f"/{user_id}/message-history",
            content=json.dumps({"message": message})
        )

        if response.status_code != status.HTTP_200_OK:
            raise AIException(
                error_code=int(response.json()["errorCode"]),
                status_code=response.status_code
            )
