import os
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


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
}
