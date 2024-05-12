from pymongo import errors
from exceptions import MessageHistoryException
from constants import ErrorCodes


def match_collection_error(e: errors.PyMongoError) -> MessageHistoryException:
    if e.timeout:
        return MessageHistoryException(ErrorCodes.DB_CONNECTION_TIMEOUT, status_code=504)
    else:
        return MessageHistoryException(ErrorCodes.DB_CONNECTION_FAILURE, status_code=500)