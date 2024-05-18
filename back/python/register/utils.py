from pymongo import errors
from exceptions import RegisterException
from constants import ErrorCodes
from fastapi import status


def match_collection_error(e: errors.PyMongoError) -> RegisterException:
    if e.timeout:
        return RegisterException(ErrorCodes.DB_CONNECTION_TIMEOUT, status_code=status.HTTP_504_GATEWAY_TIMEOUT)
    else:
        return RegisterException(ErrorCodes.DB_CONNECTION_FAILURE, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)