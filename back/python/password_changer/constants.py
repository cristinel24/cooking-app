import os
from enum import Enum
from dotenv import load_dotenv
from fastapi import status

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 2590))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
HASHER_API_URL = os.getenv("HASHER_API_URL", "http://localhost:2020")
TOKEN_VALIDATOR_API_URL = os.getenv("TOKEN_VALIDATOR_API_URL", "http://localhost:8090")
TOKEN_DESTROYER_API_URL = os.getenv("TOKEN_DESTROYER_API_URL", "http://localhost:8000")

TIMEOUT_LIMIT = 3
DESIRED_PASSWORD_CHANGE_TOKEN_TYPE = "passwordChange"


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 25900
    FAILED_TO_UPDATE_PASSWORD = 25901
    HASHER_REQUEST_FAILED = 25902
    TOKEN_VALIDATOR_REQUEST_FAILED = 25903
    TOKEN_DESTROYER_REQUEST_FAILED = 25904
    PASSWORD_REQUIRED = 25905
    PASSWORD_TOO_SHORT = 25906
    PASSWORD_TOO_LONG = 25907
    TOKEN_REQUIRED = 25908


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
    ErrorCodes.PASSWORD_REQUIRED.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.PASSWORD_TOO_SHORT.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.PASSWORD_TOO_LONG.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.TOKEN_REQUIRED.value: status.HTTP_400_BAD_REQUEST,
}

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64

PASSWORD_VALIDATION = {
    "required": ErrorCodes.PASSWORD_REQUIRED.value,
    "min_length": PASSWORD_MIN_LENGTH,
    "too_short": ErrorCodes.PASSWORD_TOO_SHORT.value,
    "max_length": PASSWORD_MAX_LENGTH,
    "too_long": ErrorCodes.PASSWORD_TOO_LONG.value,
}

TOKEN_VALIDATION = {
    "required": ErrorCodes.TOKEN_REQUIRED.value,
}
