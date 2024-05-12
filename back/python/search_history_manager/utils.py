from pymongo import errors
from exceptions import SearchHistoryException
from constants import ErrorCodes


def match_collection_error(e: errors.PyMongoError) -> SearchHistoryException:
    if e.timeout:
        return SearchHistoryException(ErrorCodes.DB_CONNECTION_TIMEOUT, status_code=504)
    else:
        return SearchHistoryException(ErrorCodes.DB_CONNECTION_FAILURE, status_code=500)
