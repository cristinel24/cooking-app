import nh3
from fastapi import status
from pymongo import errors

from constants import *
from exception import RecipeEditorException
from schemas import RecipeData


class Actions:
    INCREMENT = 1
    DECREMENT = -1


def validate_recipe_data(recipe_data: RecipeData):
    if recipe_data.title is not None and not 8 <= len(recipe_data.title) <= 128:
        raise RecipeEditorException(ErrorCodes.INVALID_TITLE_SIZE.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.description is not None:
        if not 80 <= len(recipe_data.description) <= 10_000:
            raise RecipeEditorException(ErrorCodes.INVALID_DESCRIPTION_SIZE.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.prepTime is not None and recipe_data.prepTime % 5 != 0 or recipe_data.prepTime == 0:
        raise RecipeEditorException(ErrorCodes.INVALID_PREPTIME.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.steps is not None:
        if not recipe_data.steps:
            raise RecipeEditorException(ErrorCodes.EMPTY_LIST_STEPS.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.ingredients is not None and not recipe_data.ingredients:
        raise RecipeEditorException(ErrorCodes.EMPTY_LIST_INGREDIENTS.value, status.HTTP_400_BAD_REQUEST)
    if recipe_data.thumbnail is not None and not 0 <= len(recipe_data.thumbnail) <= 2048:
        raise RecipeEditorException(ErrorCodes.INVALID_THUMBNAIL_URL_SIZE.value, status.HTTP_400_BAD_REQUEST)


def check_flags(flags: int, n: int) -> bool:
    return (flags & (1 << n)) == 1


def match_collection_error(e: errors.PyMongoError) -> RecipeEditorException:
    if e.timeout:
        return RecipeEditorException(ErrorCodes.DB_CONNECTION_TIMEOUT.value, status.HTTP_504_GATEWAY_TIMEOUT)
    else:
        return RecipeEditorException(ErrorCodes.DB_CONNECTION_NONTIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)


def sanitize_html(fields: dict[str, str | list[str]]) -> dict[str, str | list[str]]:
    clean_fields = dict()
    for key, value in fields.items():
        if isinstance(value, list):
            clean_htmls = list()
            for item in value:
                clean_htmls.append(
                    nh3.clean(html=item, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, url_schemes=URL_SCHEMES))
                if not clean_htmls[-1]:
                    raise RecipeEditorException(ErrorCodes.MALFORMED_HTML.value, status.HTTP_400_BAD_REQUEST)

            clean_fields[key] = clean_htmls
        elif isinstance(value, str):
            clean_fields[key] = nh3.clean(html=value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                                          url_schemes=URL_SCHEMES)
            if not clean_fields[key]:
                raise RecipeEditorException(ErrorCodes.MALFORMED_HTML.value, status.HTTP_400_BAD_REQUEST)

    return clean_fields
