import httpx  # asynchronous HTTP client for Python
from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from starlette import status

from constants import *
from exceptions import RecipeRatingManagerException
from schemas import *


async def get_previous_ratings_external(parent_id: str, start: int = Query(0),
                                        count: int = Query(10)) -> RatingListResponse:
    try:
        formatted_url = f"{RATING_MANAGER_API_URL}/{parent_id}/replies?start={start}&count={count}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url=formatted_url)
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                                                   error.get("message", "An error occurred with the Rating Manager"))

            parsed_response = RatingListResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, status.HTTP_503_SERVICE_UNAVAILABLE)

async def patch_rating_external(rating_id: str, rating_data: RatingUpdateRequest) -> None | JSONResponse:
    try:
        url = f"{RATING_MANAGER_API_URL}/{rating_id}"

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=rating_data.dict())
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(
                    error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                    error.get("message", "An error occurred with the Rating Manager")
                )
            return JSONResponse(content={"message": "Successful operation"}, status_code=response.status_code)
    except Exception:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, status.HTTP_503_SERVICE_UNAVAILABLE)

async def delete_rating_external(url: str, rating_id: str) -> None | JSONResponse:
    full_url = f"{url}/{rating_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(full_url)
            if response.status_code != status.HTTP_200_OK:
                raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value,
                                                   "An error occurred with the Rating Manager")

            return JSONResponse(content={"message": "Successful operation"}, status_code=response.status_code)
        except Exception:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, "Internal Server Error")

async def create_rating_external(parent_id: str, rating_data: RatingCreateRequest) -> None | JSONResponse:
    try:
        formatted_url = f"{RATING_MANAGER_API_URL}/{parent_id}/replies"

        async with httpx.AsyncClient() as client:
            response = await client.post(url=formatted_url, json=rating_data.dict())
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(
                    error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                    error.get("message", "An error occurred with the Rating Manager")
                )
            return JSONResponse(content={"message": "Successful operation"}, status_code=response.status_code)
    except Exception:
        raise HTTPException(status_code=ErrorCodes.INTERNAL_SERVER_ERROR.value, detail="Internal Server Error")




