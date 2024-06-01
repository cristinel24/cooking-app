from fastapi import status
from fastapi.responses import JSONResponse
from pymongo import errors

from constants import ErrorCodes
from exceptions import SearchHistoryException


def match_collection_error(e: errors.PyMongoError) -> SearchHistoryException:
    if e.timeout:
        return SearchHistoryException(ErrorCodes.DB_CONNECTION_TIMEOUT, status_code=status.HTTP_504_GATEWAY_TIMEOUT)
    else:
        return SearchHistoryException(ErrorCodes.DB_CONNECTION_FAILURE,
                                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_error_json_response(status_code: int, error_code: ErrorCodes) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"errorCode": error_code.value})
