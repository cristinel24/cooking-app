import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
MONGO_TIMEOUT = 3

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://0.0.0.0:8001")
ID_GENERATOR_ROUTE = "/"

HASHER_API_URL = os.getenv("HASHER_API_URL", "http://0.0.0.0:8002")
HASHER_ROUTE = "/target"

TOKEN_GENERATOR_API_URL = os.getenv("TOKEN_GENERATOR_API_URL", "http://0.0.0.0:8003")
TOKEN_GENERATOR_ROUTE = "/{user_id}/{token_type}"

EMAIL_SYSTEM_API_URL = os.getenv("EMAIL_SYSTEM_API_URL", "http://0.0.0.0:8004")
EMAIL_SYSTEM_ROUTE = "/verify-account"

TOKEN_DESTROYER_API_URL = os.getenv("TOKEN_DESTROYER_API_URL", "http://0.0.0.0:8005")
TOKEN_DESTROYER_ROUTE = "/{token}"

USER_DESTROYER_API_URL = os.getenv("USER_DESTROYER_API_URL", "http://0.0.0.0:8006")
DESTROY_USER_ROUTE = "/{user_id}"

VERIFY_ACCOUNT_TOKEN_TYPE = "emailChange"

EMPTY_USER_DATA = {
    "email": None,
    "roles": 0,
    "ratingSum": 0,
    "ratingCount": 0,
    "description": "",
    "messageHistory": [],
    "searchHistory": [],
    "recipes": [],
    "allergens": [],
    "ratings": [],
    "savedRecipes": []
}


class ErrorCodes(Enum):
    USERNAME_EXISTS = 25400
    PASSWORD_HASHING_FAILED = 25401
    DATABASE_ERROR = 25402
    DATABASE_TIMEOUT = 25403
    TOKEN_GENERATION_FAILED = 25404
    USER_DATA_VALIDATION_ERROR = 25405
    EMAIL_SENDING_FAILED = 25406
    DATABASE_CONNECTION_ERROR = 25407
    ID_GENERATION_FAILED = 25408
    DB_INSERTION_ERROR = 25409
    SERVER_ERROR = 25410
    DISPLAY_NAME_TOO_SHORT = 25411
    DISPLAY_NAME_TOO_LONG = 25412
    EMAIL_TOO_LONG = 25413
    USERNAME_INVALID = 25414
    USERNAME_TOO_SHORT = 25415
    USERNAME_TOO_LONG = 25416
    USERNAME_REQUIRED = 25417
    EMAIL_REQUIRED = 25418
    PASSWORD_TOO_SHORT = 25419
    PASSWORD_TOO_LONG = 25420
    PASSWORD_REQUIRED = 25421
    MALFORMED_DESCRIPTION = 25422
    USER_DESTROY_FAILED = 25423
    TOKEN_DESTROY_FAILED = 25424
    EMAIL_INVALID = 25425


USERNAME_MIN_LENGTH = 8
USERNAME_MAX_LENGTH = 64
USERNAME_REGEX = r"[A-Za-z0-9_\.]+"
EMAIL_REGEX = r".*@.*"
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64
DISPLAY_NAME_MIN_LENGTH = 4
DISPLAY_NAME_MAX_LENGTH = 64

DISPLAY_NAME_VALIDATION = {
    "min_length": DISPLAY_NAME_MIN_LENGTH,
    "max_length": DISPLAY_NAME_MAX_LENGTH,
    "too_short": ErrorCodes.DISPLAY_NAME_TOO_SHORT.value,
    "too_long": ErrorCodes.DISPLAY_NAME_TOO_LONG.value,
}

EMAIL_VALIDATION = {
    "required": ErrorCodes.EMAIL_REQUIRED.value,
    "too_long": ErrorCodes.EMAIL_TOO_LONG.value,
    "pattern": {"regex": EMAIL_REGEX, "error": ErrorCodes.EMAIL_INVALID.value}
}

USERNAME_VALIDATION = {
    "pattern": {"regex": USERNAME_REGEX, "error": ErrorCodes.USERNAME_INVALID.value},
    "min_length": USERNAME_MIN_LENGTH,
    "max_length": USERNAME_MAX_LENGTH,
    "too_short": ErrorCodes.USERNAME_TOO_SHORT.value,
    "too_long": ErrorCodes.USERNAME_TOO_LONG.value,
    "required": ErrorCodes.USERNAME_REQUIRED.value
}

PASSWORD_VALIDATION = {
    "min_length": PASSWORD_MIN_LENGTH,
    "max_length": PASSWORD_MAX_LENGTH,
    "too_short": ErrorCodes.PASSWORD_TOO_SHORT.value,
    "too_long": ErrorCodes.PASSWORD_TOO_LONG.value,
    "required": ErrorCodes.PASSWORD_REQUIRED.value
}
