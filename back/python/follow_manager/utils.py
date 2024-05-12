from pymongo import errors
from fastapi import status

from constants import ErrorCodes
from exception import FollowManagerException


def match_collection_error(e: errors.PyMongoError) -> FollowManagerException:
    if e.timeout:
        return FollowManagerException(ErrorCodes.DB_CONNECTION_TIMEOUT, status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return FollowManagerException(ErrorCodes.DB_CONNECTION_NONTIMEOUT, status.HTTP_500_INTERNAL_SERVER_ERROR)
