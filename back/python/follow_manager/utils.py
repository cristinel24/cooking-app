from pymongo import errors

from constants import ErrorCodes
from exception import FollowManagerException


def match_collection_error(e: errors.PyMongoError) -> FollowManagerException:
    if e.timeout:
        return FollowManagerException(ErrorCodes.DB_CONNECTION_TIMEOUT, 500)
    else:
        return FollowManagerException(ErrorCodes.DB_CONNECTION_NONTIMEOUT, status_code=500)
