from fastapi import status
from pymongo import errors

from constants import ErrorCodes
from exception import RecipeCreatorException
from schemas import RecipeData


def validate_recipe_data(recipe_data: RecipeData):
    if not 8 <= len(recipe_data.title) <= 128:
        raise RecipeCreatorException(ErrorCodes.INVALID_TITLE_SIZE.value, status.HTTP_400_BAD_REQUEST)
    if not 80 <= len(recipe_data.description) <= 10_000:
        raise RecipeCreatorException(ErrorCodes.INVALID_DESCRIPTION_SIZE.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.prepTime % 5 != 0 or recipe_data.prepTime == 0:
        raise RecipeCreatorException(ErrorCodes.INVALID_PREPTIME.value, status.HTTP_400_BAD_REQUEST)
    if not recipe_data.steps:
        raise RecipeCreatorException(ErrorCodes.EMPTY_LIST_STEPS.value, status.HTTP_400_BAD_REQUEST)
    if not recipe_data.ingredients:
        raise RecipeCreatorException(ErrorCodes.EMPTY_LIST_INGREDIENTS.value, status.HTTP_400_BAD_REQUEST)
    if not 0 <= len(recipe_data.thumbnail) <= 2048:
        raise RecipeCreatorException(ErrorCodes.INVALID_THUMBNAIL_URL_SIZE.value, status.HTTP_400_BAD_REQUEST)


def check_flags(flags: int, n: int) -> bool:
    return (flags & (1 << n)) == 1


def match_collection_error(e: errors.PyMongoError) -> RecipeCreatorException:
    if e.timeout:
        return RecipeCreatorException(ErrorCodes.DB_CONNECTION_TIMEOUT.value, status.HTTP_504_INTERNAL_SERVER_ERROR)
    else:
        return RecipeCreatorException(ErrorCodes.DB_CONNECTION_NONTIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
