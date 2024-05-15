from repository import *
from schemas import *
import exceptions
from api import *

recipe_collection = RecipeCollection()


async def get_recipe_by_id(recipe_id: str) -> RecipeData:
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id, RECIPE_DATA_PROJECTION)
    if not recipe_data:
        raise exceptions.RecipeException(ErrorCodes.NONEXISTENT_RECIPE.value)
    author_id = recipe_data.get("authorId")
    user_card = await request_user_card(author_id)
    recipe_data["author"] = user_card
    return recipe_data


async def get_recipe_card_by_id(recipe_id: str) -> RecipeCardData:
    recipe_card = recipe_collection.get_recipe_by_id(recipe_id, RECIPE_DATA_CARD_PROJECTION)
    if not recipe_card:
        raise exceptions.RecipeException(ErrorCodes.NONEXISTENT_RECIPE.value)
    author_id = recipe_card.get("authorId")
    user_card = await request_user_card(author_id)
    recipe_card["author"] = user_card
    return recipe_card
