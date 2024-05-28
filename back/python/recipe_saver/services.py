import httpx

import api
from constants import ErrorCodes
from repository import UserCollection
from schemas import RecipeCardsRequest, RecipeCardData
from exceptions import RecipeSaverException
from fastapi import status

user_collection = UserCollection()


def save_recipe(user_id: str, recipe_id: str):
    user_collection.add_recipe_to_user(user_id, recipe_id)


async def get_recipes(user_id: str, start: int, count: int) -> list[RecipeCardData]:
    saved_recipes = list(user_collection.get_saved_recipes(user_id, start, count))
    try:
        saved_recipes_cards = (await api.request_recipe_cards(RecipeCardsRequest(ids=saved_recipes))).recipeCards
    except httpx.ConnectError:
        raise RecipeSaverException(ErrorCodes.NON_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)

    ordered_saved_recipe_cards = [[recipe_card for recipe_card in saved_recipes_cards if recipe_card.id == recipe_id][0]
                                  for recipe_id in saved_recipes]

    return ordered_saved_recipe_cards


def remove_recipe_from_saved(user_id: str, recipe_id: str):
    user_collection.remove_recipe_from_saved(user_id, recipe_id)
