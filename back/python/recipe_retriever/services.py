from repository import *
from schemas import *
import exceptions
from api import *
from fastapi import status

recipe_collection = RecipeCollection()


async def get_recipe_by_id(recipe_id: str) -> RecipeData:
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id, RECIPE_DATA_PROJECTION, True)
    if not recipe_data:
        raise exceptions.RecipeException(status.HTTP_404_NOT_FOUND_NOT_FOUND, ErrorCodes.NONEXISTENT_RECIPE)

    author_id = str(recipe_data.get("authorId"))
    recipe_data.pop("authorId")
    user_card = await request_user_card(author_id)
    recipe_data["ratingAvg"] = (
            recipe_data["ratingSum"] / recipe_data["ratingCount"]) if recipe_data["ratingSum"] > 0 else 0
    recipe_data.pop("ratingSum")
    recipe_data.pop("ratingCount")
    recipe_data["author"] = user_card

    return RecipeData(**recipe_data)


async def get_recipe_card_by_id(recipe_id: str) -> RecipeCardData:
    recipe_card = recipe_collection.get_recipe_by_id(recipe_id, RECIPE_DATA_CARD_PROJECTION, False)
    if not recipe_card:
        raise exceptions.RecipeException(status.HTTP_404_NOT_FOUND_NOT_FOUND, ErrorCodes.NONEXISTENT_RECIPE)

    author_id = str(recipe_card.get("authorId"))
    recipe_card.pop("authorId")
    user_card = await request_user_card(author_id)
    recipe_card["ratingAvg"] = (
            recipe_card["ratingSum"] / recipe_card["ratingCount"]) if recipe_card["ratingSum"] > 0 else 0
    recipe_card.pop("ratingSum")
    recipe_card.pop("ratingCount")
    recipe_card["author"] = user_card

    return RecipeCardData(**recipe_card)
