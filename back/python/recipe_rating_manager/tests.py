import asyncio
from typing import Optional
from unittest.mock import MagicMock
from starlette.requests import Request

import httpx
from fastapi import FastAPI, HTTPException
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

from constants import *
from exceptions import *
from schemas import *

RATING_MANAGER_API_URL = os.getenv("RATING_MANAGER_API_URL", "http://localhost:8001")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://localhost:8002")
ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://localhost:8003")


class UserCardData(BaseModel):
    id: str
    username: str
    email: str
    icon: str
    displayName: str
    roles: int


class RatingData(BaseModel):
    parentId: str
    parentType: str
    author: UserCardData
    updatedAt: str
    rating: int
    description: str


class RatingListResponse(BaseModel):
    ratings: List[RatingData]
    total: int


async def get_ratings_from_service(parent_id: str, request: Request, start: int = 0,
                                   count: int = 10) -> RatingListResponse:
    user_id = request.state.user_id
    user_roles = request.state.user_roles

    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized: User is not authenticated")

    url = f"{RATING_MANAGER_API_URL}/rating/{parent_id}/replies"
    params = {"start": start, "count": count}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)

            if response.status_code != 200:
                error = response.json()
                raise RecipeRatingManagerException(
                    error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                    error.get("message", "An error occurred with the Rating Manager")
                )

            response_json = response.json()
            rating_list_response = RatingListResponse(**response_json)
            return rating_list_response

        except httpx.HTTPStatusError as e:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value,
                                               f"HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.ConnectError as e:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, f"Connection error: {str(e)}")
        except httpx.RequestError as e:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value,
                                               f"Request error: {e.request.url!r}: {e}")
        except Exception:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, "Internal Server Error")


# Test function

async def test_get_ratings():
    parent_id = "c5"
    scope = {"type": "http", "path": "/", "headers": {}}
    dummy_request = Request(scope)

    # Add user_id and user_roles to the request state
    dummy_request.state.user_id = "1"
    dummy_request.state.user_roles = ["Admin"]

    try:
        ratings_response = await get_ratings_from_service(parent_id, dummy_request)
        print(f"Total ratings found: {ratings_response.total}")
        for rating in ratings_response.ratings:
            print(f"Rating: {rating.description} by author {rating.authorId}")
    except RecipeRatingManagerException as e:
        print(f"Error occurred: {e.message} (Error code: {e.error_code})")


# Run the test
if __name__ == "__main__":
    asyncio.run(test_get_ratings())


async def delete_rating(url: str, rating_id: str):
    full_url = f"{url}/rating/{rating_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(full_url)
            response.raise_for_status()  # Raise an exception for 4xx/5xx responses
            print(f"Server responded with status code: {response.status_code}")
            print(f"Response content: {response.text}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except httpx.ConnectError as e:
            print(f"Connection error: {str(e)}")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")


# Usage example
async def test_delete_rating():
    url = RATING_MANAGER_API_URL
    rating_id = "fl"  # Replace with an actual rating ID
    await delete_rating(url, rating_id)
