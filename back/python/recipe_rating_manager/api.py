import httpx  # asynchronous HTTP client for Python

from schemas import *
from constants import *
from starlette import status
from exceptions import RecipeRatingManagerException

async def delete_rating(url: str, rating_id: str):
    full_url = f"{url}/rating/{rating_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(full_url)
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR.value),
                                                   error.get("message", "An error occurred with the Rating Manager"))
            return response.status_code
        except Exception:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, "Internal Server Error")


async def update_recipe_rating(recipe_id: str, user_id: str, rating_data: RatingCreateRequest):
    try:
        url = f"{RATING_MANAGER_API_URL}/rating/{recipe_id}/replies"
        headers = {
            "user_id": user_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(url, json=rating_data.dict(), headers=headers)
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                                                   error.get("message", "An error occurred with the Rating Manager"))
            return response.json()
    except Exception:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def update_rating(rating_id: str, user_id: str, rating_data: RatingUpdateRequest):
    try:
        url = f"{RATING_MANAGER_API_URL}/rating/{rating_id}"
        headers = {
            "user_id": user_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=rating_data.dict(), headers=headers)
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR.value),
                                                   error.get("message", "An error occurred with the Rating Manager"))
            return response.json()
    except Exception:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def get_ratings(parent_id: str, start: int, count: int, user_id: str) -> RatingListResponse:
    try:
        url = f"{RATING_MANAGER_API_URL}/rating/{parent_id}/replies"
        headers = {
            "user_id": user_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"start": start, "count": count}, headers=headers)
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                                                   error.get("message", "An error occurred with the Rating Manager"))
            response_json = response.json()
            return RatingListResponse(**response_json)
    except Exception:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, status.HTTP_503_SERVICE_UNAVAILABLE)
