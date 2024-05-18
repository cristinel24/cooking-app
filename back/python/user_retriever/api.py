import httpx
from constants import FOLLOW_MANAGER_API_URL, FOLLOWERS_COUNT_ROUTE, FOLLOWING_COUNT_ROUTE, ErrorCodes
from exception import UserRetrieverException
from fastapi import status


async def request_user_followers_count(user_id: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=FOLLOW_MANAGER_API_URL + f"/{user_id}" + FOLLOWERS_COUNT_ROUTE)
        if response.status_code != status.HTTP_200_OK:
            raise UserRetrieverException(response.status_code, response.json()["errorCode"])
        return response.json()["followersCount"]


async def request_user_following_count(user_id: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=FOLLOW_MANAGER_API_URL + f"/{user_id}" + FOLLOWING_COUNT_ROUTE)
        if response.status_code != status.HTTP_200_OK:
            raise UserRetrieverException(response.status_code, response.json()["errorCode"])
        return response.json()["followingCount"]
