from typing import Union

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
            parsed_response = RatingListResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise RecipeRatingManagerException(ErrorCodes.INTERNAL_SERVER_ERROR.value, status.HTTP_503_SERVICE_UNAVAILABLE)



from fastapi import FastAPI, HTTPException, Query
from fastapi import Request
from fastapi.responses import JSONResponse



app = FastAPI()


async def get_ratings_microservice(parent_id: str, start: int, count: int) -> RatingListResponse:
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


@app.get("/rating/{parent_id}/replies", response_model=RatingListResponse, response_description="Successful operation")
async def get_ratings_route(parent_id: str, start: int = Query(0),
                            count: int = Query(10)) -> RatingListResponse | JSONResponse:
    return await get_ratings_microservice(parent_id, start, count)

if __name__ == "__main__":
    import uvicorn
    PORT = 2233
    uvicorn.run(app, host=HOST, port=PORT)
