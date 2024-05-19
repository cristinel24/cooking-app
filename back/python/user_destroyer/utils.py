from pymongo import errors

from constants import ErrorCodes
from exception import UserDestroyerException


def match_collection_error(e: errors.PyMongoError) -> UserDestroyerException:
    if e.timeout:
        return UserDestroyerException(ErrorCodes.DB_CONNECTION_TIMEOUT, 500)
    else:
        return UserDestroyerException(ErrorCodes.DB_CONNECTION_NONTIMEOUT, status_code=500)
