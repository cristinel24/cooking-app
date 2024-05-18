from pymongo import errors
from exceptions import SearchHistoryException
from constants import ErrorCodes

from fastapi import status

def match_collection_error(e: errors.PyMongoError) -> SearchHistoryException:
    if e.timeout:
        return SearchHistoryException(ErrorCodes.DB_CONNECTION_TIMEOUT, status_code=status.HTTP_504_GATEWAY_TIMEOUT)
    else:
        return SearchHistoryException(ErrorCodes.DB_CONNECTION_FAILURE, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
