import httpx
from fastapi import status

from constants import ErrorCodes, RECIPE_RETRIEVER_API_URL
from exceptions import RecipeSaverException
from schemas import RecipeCardsRequest, RecipeCardsResponse, RecipeCardData


async def request_recipe_cards(recipe_ids: RecipeCardsRequest) -> RecipeCardsResponse:
    async with httpx.AsyncClient() as client:
        payload = recipe_ids.model_dump_json()
        response = await client.post(url=f"{RECIPE_RETRIEVER_API_URL}/cards",
                                     content=payload)
        recipe_cards_response = RecipeCardsResponse(recipeCards=[])
        if "recipeCards" not in response.json():
            if "errorCode" in response.json():
                raise RecipeSaverException(int(response.json()["errorCode"]), status.HTTP_404_NOT_FOUND)
            else:
                raise RecipeSaverException(ErrorCodes.NON_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            recipe_cards_response.recipeCards = [RecipeCardData(**card) for card in response.json()["recipeCards"]]
        return recipe_cards_response
