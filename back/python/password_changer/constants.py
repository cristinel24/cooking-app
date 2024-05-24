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
    TOKEN_VALIDATOR_REQUEST_FAILED = 25803
    TOKEN_DESTROYER_REQUEST_FAILED = 25804


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
}
