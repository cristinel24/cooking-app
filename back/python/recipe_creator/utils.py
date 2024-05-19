from fastapi import status
from pymongo import errors

from constants import ErrorCodes
from exception import RecipeCreatorException
from schemas import RecipeData


def validate_recipe_data(recipe_data: RecipeData) -> bool:
    return (
        8 <= len(recipe_data.title) <= 128 and
        80 <= len(recipe_data.description) <= 10_000 and
        recipe_data.prepTime % 5 == 0 and
        len(recipe_data.steps) > 0 and
        len(recipe_data.ingredients) > 0 and
        0 <= len(recipe_data.thumbnail) <= 2048
    )


def check_flags(flags: int, n: int) -> bool:
    return (flags & (1 << n)) == 1


def match_collection_error(e: errors.PyMongoError) -> RecipeCreatorException:
    if e.timeout:
        return RecipeCreatorException(ErrorCodes.DB_CONNECTION_TIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return RecipeCreatorException(ErrorCodes.DB_CONNECTION_NONTIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
