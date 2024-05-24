import os
from enum import Enum
from dotenv import load_dotenv
from fastapi import status

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 2590))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")

TIMEOUT_LIMIT = 3
DESIRED_PASSWORD_CHANGE_TOKEN_TYPE = "passwordChange"


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 25900
    FAILED_TO_GET_TOKEN_TYPE = 25901
    TOKEN_NOT_FOUND = 25902
    FAILED_TO_GET_USER_ID = 25903
    USER_NOT_FOUND = 25904
    FAILED_TO_UPDATE_PASSWORD = 25905
    FAILED_TO_DESTROY_TOKENS = 25906
    INVALID_TOKEN_TYPE = 25907
    PASSWORD_HASH_REQUEST_FAILED = 25908


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
    ErrorCodes.TOKEN_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
    ErrorCodes.USER_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
    ErrorCodes.INVALID_TOKEN_TYPE.value: status.HTTP_403_FORBIDDEN,
}
