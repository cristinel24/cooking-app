from pymongo import errors

from constants import ErrorCodes
from exception import TokenDestroyerException


def match_collection_error(e: errors.PyMongoError) -> TokenDestroyerException:
    if e.timeout:
        return TokenDestroyerException(ErrorCodes.DB_CONNECTION_TIMEOUT, 500)
    else:
        return TokenDestroyerException(ErrorCodes.DB_CONNECTION_NONTIMEOUT, status_code=500)