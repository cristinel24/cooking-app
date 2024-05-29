from fastapi import status
from pymongo import errors

from constants import ErrorCodes, logger
from exception import RecipeDestroyerException


def match_collection_error(e: errors.PyMongoError) -> RecipeDestroyerException:
    logger.error(e)
    if e.timeout:
        return RecipeDestroyerException(
            error_code=ErrorCodes.DB_TIMEOUT.value,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return RecipeDestroyerException(ErrorCodes.DB_NON_TIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
