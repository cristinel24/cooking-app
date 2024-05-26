import os
from enum import Enum
from dotenv import load_dotenv
from fastapi import status

load_dotenv()

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 2600))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME")
EMAIL_SYSTEM_API_URL = os.getenv("EMAIL_SYSTEM_API_URL", "http://localhost:2060")
TOKEN_GENERATOR_API_URL = os.getenv("TOKEN_GENERATOR_API_URL", "http://localhost:8091")
TOKEN_VALIDATOR_API_URL = os.getenv("TOKEN_VALIDATOR_API_URL", "http://localhost:8090")
TOKEN_DESTROYER_API_URL = os.getenv("TOKEN_DESTROYER_API_URL", "http://localhost:8000")


TIMEOUT_LIMIT = 3
DESIRED_EMAIL_CHANGE_TOKEN_TYPE = "emailChange"
EMAIL_VERIFICATION_TOKEN_TYPE = "emailConfirm"


class ErrorCodes(Enum):
    DB_CONNECTION_FAILURE = 25900
    FAILED_TO_UPDATE_EMAIL = 25901
    TOKEN_GENERATOR_REQUEST_FAILED = 25902
    EMAIL_SYSTEM_REQUEST_FAILED = 25903
    TOKEN_VALIDATOR_REQUEST_FAILED = 25904
    TOKEN_DESTROYER_REQUEST_FAILED = 25905
    FAILED_TO_CHECK_UNIQUE_EMAIL = 25906
    EMAIL_UNIQUE_CONSTRAINT_VIOLATED = 25907


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
    ErrorCodes.EMAIL_UNIQUE_CONSTRAINT_VIOLATED.value: status.HTTP_403_FORBIDDEN
}
