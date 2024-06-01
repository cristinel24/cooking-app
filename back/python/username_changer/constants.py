import os
import re
from enum import Enum
from dotenv import load_dotenv
from fastapi import status

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 2580))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
TOKEN_VALIDATOR_API_URL = os.getenv("TOKEN_VALIDATOR_API_URL", "http://localhost:8090")
TOKEN_DESTROYER_API_URL = os.getenv("TOKEN_DESTROYER_API_URL", "http://localhost:8000")


TIMEOUT_LIMIT = 3
DESIRED_USERNAME_CHANGE_TOKEN_TYPE = "usernameChange"


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 25800
    FAILED_TO_UPDATE_USERNAME = 25801
    TOKEN_VALIDATOR_REQUEST_FAILED = 25802
    TOKEN_DESTROYER_REQUEST_FAILED = 25803
    USERNAME_REQUIRED = 25804
    USERNAME_TOO_SHORT = 25805
    USERNAME_TOO_LONG = 25806
    USERNAME_INVALID = 25807
    TOKEN_REQUIRED = 25808


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
    ErrorCodes.USERNAME_REQUIRED.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.USERNAME_TOO_SHORT.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.USERNAME_TOO_LONG.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.USERNAME_INVALID.value: status.HTTP_400_BAD_REQUEST,
    ErrorCodes.TOKEN_REQUIRED.value: status.HTTP_400_BAD_REQUEST,
}

USERNAME_MIN_LENGTH = 8
USERNAME_MAX_LENGTH = 64
USERNAME_REGEX = r"[A-Za-z0-9_\.]+"
COMPILED_USERNAME_REGEX = re.compile(USERNAME_REGEX)

USERNAME_VALIDATION = {
    "required": ErrorCodes.USERNAME_REQUIRED.value,
    "min_length": USERNAME_MIN_LENGTH,
    "too_short": ErrorCodes.USERNAME_TOO_SHORT.value,
    "max_length": USERNAME_MAX_LENGTH,
    "too_long": ErrorCodes.USERNAME_TOO_LONG.value,
    "pattern": {"regex": COMPILED_USERNAME_REGEX, "error": ErrorCodes.USERNAME_INVALID.value}
}

TOKEN_VALIDATION = {
    "required": ErrorCodes.TOKEN_REQUIRED.value
}
