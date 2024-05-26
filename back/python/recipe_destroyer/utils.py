from fastapi import status
from pymongo import errors

from constants import ErrorCodes
from exception import RecipeDestroyerException

def match_collection_error(e: errors.PyMongoError) -> RecipeDestroyerException:
    if e.timeout:
        return RecipeDestroyerException(ErrorCodes.DB_CONNECTION_TIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return RecipeDestroyerException(ErrorCodes.DB_CONNECTION_NONTIMEOUT.value, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
