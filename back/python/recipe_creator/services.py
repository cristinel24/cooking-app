import httpx
from fastapi import status

import api
from constants import ErrorCodes
from exception import RecipeCreatorException
from schemas import RecipeData, Recipe
from utils import validate_recipe_data, check_flags


async def create_recipe(user_id: str, recipe_data: RecipeData):
    if validate_recipe_data(recipe_data) is False:
        raise RecipeCreatorException(ErrorCodes.INVALID_RECIPE_DATA.value, status.HTTP_400_BAD_REQUEST)
    recipe = Recipe(recipe_data)
    try:
        recipe.id = await api.get_id()
    except httpx.ConnectError:
        raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
    recipe.tokens = await api.tokenize_recipe(recipe_data.model_dump(exclude=set("thumbnail")))
    recipe.authorId = user_id
    flags = 0b0000
    try:

        flags += 1

        flags += 1 << 1
        await api.add_allergens(recipe.allergens)
        flags += 1 << 2
        await api.add_tags(recipe.tags)
        flags += 1 << 3
    except RecipeCreatorException as e:
        if check_flags(flags, 0):
            pass
        if check_flags(flags, 1):
            pass
        if check_flags(flags, 2):
            await api.delete_allergens(recipe.allergens)
        if check_flags(flags, 3):
            await api.delete_tags(recipe.tags)
