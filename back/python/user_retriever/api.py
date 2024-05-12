import httpx
from constants import FOLLOW_MANAGER_API_URL, FOLLOWERS_COUNT_ROUTE, FOLLOWING_COUNT_ROUTE, ErrorCodes
from exception import UserRetrieverException
from fastapi import status


async def request_user_followers_count(user_id: str) -> int:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=FOLLOW_MANAGER_API_URL + f"/{user_id}" + FOLLOWERS_COUNT_ROUTE)
            return response.json()["followersCount"]
    except Exception:
        raise UserRetrieverException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     ErrorCodes.FAILED_TO_GET_USER_FOLLOWERS_COUNT)


async def request_user_following_count(user_id: str) -> int:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=FOLLOW_MANAGER_API_URL + f"/{user_id}" + FOLLOWING_COUNT_ROUTE)
            return response.json()["followingCount"]
    except Exception:
        raise UserRetrieverException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     ErrorCodes.FAILED_TO_GET_USER_FOLLOWING_COUNT)
