from enum import Enum
from fastapi import status

TIMEOUT_LIMIT = 3
DESIRED_USERNAME_CHANGE_TOKEN_TYPE = "usernameChange"


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 25800
    FAILED_TO_GET_TOKEN_TYPE = 25801
    TOKEN_NOT_FOUND = 25802
    FAILED_TO_GET_USER_ID = 25803
    USER_NOT_FOUND = 25804
    FAILED_TO_DESTROY_TOKENS = 25805
    FAILED_TO_UPDATE_USERNAME = 25806
    INVALID_TOKEN_TYPE = 25807


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
    ErrorCodes.TOKEN_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
    ErrorCodes.USER_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
    ErrorCodes.INVALID_TOKEN_TYPE.value: status.HTTP_403_FORBIDDEN,
}
