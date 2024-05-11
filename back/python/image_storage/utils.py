from constants import ErrorCodes
from exception import ImageStorageException


def match_exception(e: ImageStorageException) -> int:
    match e.error_code:
        case ErrorCodes.INVALID_IMAGE:
            return 400
        case ErrorCodes.NOT_RESPONSIVE_API:
            return 404
        case ErrorCodes.DUPLICATE_ID:
            return 400
