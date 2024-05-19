from pymongo import errors

from constants import ErrorCodes
from exception import TokenDestroyerException
from fastapi import status


def match_collection_error(e: errors.PyMongoError) -> TokenDestroyerException:
    if e.timeout:
        return TokenDestroyerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DB_CONNECTION_TIMEOUT.value)
    else:
        return TokenDestroyerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DB_CONNECTION_NONTIMEOUT.value)
