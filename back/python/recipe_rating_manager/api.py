import httpx  # asynchronous HTTP client for Python
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette import status

from constants import *
from exceptions import RecipeRatingManagerException
from schemas import *

async def get_previous_ratings_microservice(parent_id: str, start: int, count: int) -> RatingListResponse:
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

# tested, it works
# does RatingUpdateRequest also need parent_type??
async def patch_rating(rating_id: str, rating_data: RatingUpdateRequest) -> None | JSONResponse:
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

# delete_rating works
async def delete_rating(url: str, rating_id: str) -> None | JSONResponse:
    full_url = f"{url}/{rating_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(full_url)
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(
                    error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                    error.get("message", "An error occurred with the Rating Manager")
                )
            return JSONResponse(content={"message": "Successful operation"}, status_code=response.status_code)
        except Exception:
            raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, "Internal Server Error")


# perfect stuff
async def create_rating(parent_id: str, rating_data: RatingCreateRequest) -> None | JSONResponse:
    try:
        formatted_url = f"{RATING_MANAGER_API_URL}/{parent_id}/replies"

        async with httpx.AsyncClient() as client:
            response = await client.put(url=formatted_url, json=rating_data.dict())
            if response.status_code != status.HTTP_200_OK:
                error = response.json()
                raise RecipeRatingManagerException(
                    error.get("errorCode", ErrorCodes.INTERNAL_SERVER_ERROR),
                    error.get("message", "An error occurred with the Rating Manager")
                )
            return JSONResponse(content={"message": "Successful operation"}, status_code=response.status_code)
    except Exception:
        raise HTTPException(status_code=ErrorCodes.INTERNAL_SERVER_ERROR.value, detail="Internal Server Error")
