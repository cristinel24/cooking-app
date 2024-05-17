from repository import *
from schemas import *
import exceptions
from api import *
from fastapi import status

recipe_collection = RecipeCollection()


async def get_recipe_by_id(recipe_id: str) -> RecipeData:
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id, RECIPE_DATA_PROJECTION)
    if not recipe_data:
        raise exceptions.RecipeException(status.HTTP_status.HTTP_404_NOT_FOUND_NOT_FOUND,
                                         ErrorCodes.NONEXISTENT_RECIPE.value)
    author_id = recipe_data.get("authorId")
    recipe_data.pop("authorId")
    user_card = await request_user_card(author_id)
    recipe_data["author"] = user_card
    return recipe_data


async def get_recipe_card_by_id(recipe_id: str) -> RecipeCardData:
    recipe_card = recipe_collection.get_recipe_by_id(recipe_id, RECIPE_DATA_CARD_PROJECTION)
    if not recipe_card:
        raise exceptions.RecipeException(status.HTTP_status.HTTP_404_NOT_FOUND_NOT_FOUND,
                                         ErrorCodes.NONEXISTENT_RECIPE.value)
    author_id = recipe_card.get("authorId")
    recipe_card.pop("authorId")
    user_card = await request_user_card(author_id)
    recipe_card["author"] = user_card
    return recipe_card
