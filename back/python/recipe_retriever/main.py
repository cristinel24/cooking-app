from fastapi import FastAPI
from fastapi.responses import JSONResponse
import exceptions
import services
import uvicorn
from constants import *
from schemas import *

app = FastAPI(title="Recipe Retriever")


@app.get("/{recipe_id}", tags=["recipe-retriever"], response_model=RecipeData,
         response_description="Successful operation")
async def get_recipe_by_id(recipe_id: str) -> RecipeData | JSONResponse:
    try:
        recipe = await services.get_recipe_by_id(recipe_id)
        return recipe
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.get("/{recipe_id}/card", tags=["recipe-retriever"], response_model=RecipeCardData,
         response_description="Successful operation")
async def get_recipe_card_by_id(recipe_id: str) -> RecipeCardData | JSONResponse:
    try:
        recipe_card = await services.get_recipe_card_by_id(recipe_id)
        return recipe_card
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


@app.post("/cards", tags=["recipe-retriever"], response_model=RecipeCardsResponse,
          response_description="Successful operation")
async def get_recipe_cards(recipe_cards_request: RecipeCardsRequest) -> RecipeCardsResponse | JSONResponse:
    try:
        return RecipeCardsResponse(recipeCards=await services.get_recipe_cards(recipe_cards_request.ids))
    except exceptions.RecipeException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
