from typing import Annotated

import exceptions
import services
import uvicorn
from constants import *
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse
from schemas import *

app = FastAPI(title="Recipe Retriever")


@app.get("/{recipe_id}", tags=["recipe-retriever"], response_model=RecipeData, response_description="Successful operation")
async def get_recipe_by_id(recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> RecipeData | JSONResponse:
    try:
        recipe = await services.get_recipe_by_id(recipe_id, x_user_id)
        return recipe
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})

@app.get("/users/{user_id}/recipes", tags=["recipe-retriever"], response_model=RecipeCardsData, response_description="Successful operation")
async def get_recipes_by_user_id(user_id: str, x_user_id: Annotated[str | None, Header()], start: int = 0, count: int = 10) -> RecipeCardsData | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHENTICATED.value})

    if user_id != x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.UNAUTHORIZED.value})

    try:
        recipes = await services.get_recipes_by_user_id(user_id, x_user_id, start, count)
        return recipes
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})

@app.get("/users/{user_id}/following/recipes", tags=["recipe-retriever"], response_model=RecipeCardsData, response_description="Successful operation")
async def get_recipes_from_followers(user_id: str, x_user_id: Annotated[str | None, Header()], start: int = 0, count: int = 10) -> RecipeCardsData | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHENTICATED.value})

    if user_id != x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.UNAUTHORIZED.value})

    try:
        recipes = await services.get_recipes_from_followers(user_id, x_user_id, start, count)
        return recipes
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})

@app.get("/{recipe_id}/card", tags=["recipe-retriever"], response_model=RecipeCardData, response_description="Successful operation")
async def get_recipe_card_by_id(recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> RecipeCardData | JSONResponse:
    try:
        recipe_card = await services.get_recipe_card_by_id(recipe_id, x_user_id)
        return recipe_card
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.post("/cards", tags=["recipe-retriever"], response_model=RecipeCardsResponse,
          response_description="Successful operation")
async def get_recipe_cards(recipe_cards_request: RecipeCardsRequest, x_user_id: Annotated[str | None, Header()] = None) -> RecipeCardsResponse | JSONResponse:
    try:
        return RecipeCardsResponse(recipeCards=await services.get_recipe_cards(recipe_cards_request.ids, x_user_id))
    except exceptions.RecipeException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
