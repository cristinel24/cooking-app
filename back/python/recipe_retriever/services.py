import httpx

from api import *
from repository import *

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


async def get_recipe_cards(recipe_ids: list[str]) -> list[RecipeCardData]:
    recipe_cards = recipe_collection.get_recipes(recipe_ids, RECIPE_DATA_CARD_PROJECTION)
    if not recipe_cards:
        return []

    author_ids = [recipe_card["authorId"] for recipe_card in recipe_cards]

    try:
        user_cards = (await request_user_cards(UserCardRequestData(ids=author_ids))).cards
    except httpx.ConnectError:
        raise RecipeException(ErrorCodes.NON_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)

    for recipe_card in recipe_cards:
        recipe_card["author"] = (
            next((user_card for user_card in user_cards if user_card.id == recipe_card["authorId"]), None))
        if not recipe_card["author"]:
            raise RecipeException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  error_code=ErrorCodes.BROKEN_USER_RETRIEVER_RESPONSE)

        recipe_card.pop("authorId")
        recipe_card["ratingAvg"] = (
                recipe_card["ratingSum"] / recipe_card["ratingCount"]) if recipe_card["ratingSum"] > 0 else 0
        recipe_card.pop("ratingSum")
        recipe_card.pop("ratingCount")

    return [RecipeCardData(**recipe_card) for recipe_card in recipe_cards]
