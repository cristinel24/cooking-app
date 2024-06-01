from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Header

import services
from constants import HOST, PORT
from schemas import *
from utils import *

app = FastAPI(title="Rating Manager")


@app.get("/{parent_type}/{parent_id}/comments", response_model=RatingList, response_description="Successful operation")
async def get(
        parent_type: str, parent_id: str, start: int,
        count: int, filter: str = "", sort: str = ""
) -> RatingList | JSONResponse:
    if start is None:
        return build_response_from_values(
            status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCodes.MISSING_START_QUERY_PARAM.value
        )

    if count is None:
        return build_response_from_values(
            status_code=status.HTTP_400_BAD_REQUEST, error_code=ErrorCodes.MISSING_COUNT_QUERY_PARAM.value
        )

    try:
        return await services.get_ratings(parent_type, parent_id, start, count, filter, sort)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


@app.get("/{rating_id}", response_model=RatingDataCard, response_description="Successful operation")
async def get_rating(rating_id: str) -> RatingDataCard | JSONResponse:
    try:
        return await services.get_rating(rating_id)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


@app.get("/", response_model=RatingDataCard, response_description="Successful operation")
async def get_rating_by_recipe_and_author_id(recipe_id: str, author_id: str) -> RatingDataCard | JSONResponse:
    try:
        return await services.get_rating_by_author_and_recipe_id(recipe_id, author_id)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


@app.post("/", response_model=None, response_description="Successful operation")
async def post_rating(body: RatingCreate, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)
    try:
        await services.post(x_user_id, body)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


@app.patch("/{rating_id}", response_model=None, response_description="Successful operation")
async def modify_rating(
        rating_id: str, body: RatingUpdate,
        x_user_id: Annotated[str | None, Header()] = None
) -> None | JSONResponse:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)

    try:
        await services.modify(x_user_id, rating_id, body)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


@app.delete("/{rating_id}", response_model=None, response_description="Successful operation")
async def delete_rating(rating_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)

    try:
        services.delete(x_user_id, rating_id)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


@app.delete("/recipes/{recipe_id}/ratings", response_model=None, response_description="Successful operation")
async def delete_all(recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)

    try:
        services.delete_all(x_user_id, recipe_id)
    except Exception as e:
        return build_response_from_exception(transform_exception(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
