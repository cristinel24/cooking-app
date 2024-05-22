from fastapi import status
from pymongo import errors
from html_sanitizer import Sanitizer
from typing import List

from constants import ErrorCodes
from exception import RecipeEditorException
from schemas import RecipeData

sanitizer = Sanitizer()


def is_string_sanitized(string: str) -> bool:
    return sanitizer.sanitize(string) == string


def validate_recipe_data(recipe_data: RecipeData):
    if recipe_data.title is not None and not 8 <= len(recipe_data.title) <= 128:
        raise RecipeEditorException(ErrorCodes.INVALID_TITLE_SIZE.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.description is not None:
        if not 80 <= len(recipe_data.description) <= 10_000:
            raise RecipeEditorException(ErrorCodes.INVALID_DESCRIPTION_SIZE.value, status.HTTP_400_BAD_REQUEST)
        if not is_string_sanitized(recipe_data.description):
            raise RecipeEditorException(ErrorCodes.MALFORMED_DESCRIPTION.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.prepTime is not None and recipe_data.prepTime % 5 != 0 or recipe_data.prepTime == 0:
        raise RecipeEditorException(ErrorCodes.INVALID_PREPTIME.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.steps is not None:
        if not recipe_data.steps:
            raise RecipeEditorException(ErrorCodes.EMPTY_LIST_STEPS.value, status.HTTP_400_BAD_REQUEST)
        for item in recipe_data.steps:
            if not is_string_sanitized(item):
                raise RecipeEditorException(ErrorCodes.MALFORMED_STEPS.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.ingredients is not None and not recipe_data.ingredients:
        raise RecipeEditorException(ErrorCodes.EMPTY_LIST_INGREDIENTS.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.thumbnail is not None and not 0 <= len(recipe_data.thumbnail) <= 2048:
        raise RecipeEditorException(ErrorCodes.INVALID_THUMBNAIL_URL_SIZE.value, status.HTTP_400_BAD_REQUEST)


def check_flags(flags: int, n: int) -> bool:
    return (flags & (1 << n)) == 1


def match_collection_error(e: errors.PyMongoError) -> RecipeEditorException:
    if e.timeout:
        return RecipeEditorException(ErrorCodes.DB_CONNECTION_TIMEOUT.value, status.HTTP_504_INTERNAL_SERVER_ERROR)
    else:
        return RecipeEditorException(ErrorCodes.DB_CONNECTION_NONTIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
