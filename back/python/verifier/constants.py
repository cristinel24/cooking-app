import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")
MONGO_TIMEOUT = 3
TOKEN_VALIDATOR_API_URL = os.getenv("TOKEN_VALIDATOR_API_URL", "http://0.0.0.0:8001")
TOKEN_DESTROYER_API_URL = os.getenv("TOKEN_DESTROYER_API_URL", "http://0.0.0.0:8002")
VERIFY_TOKEN_ROUTE = os.getenv("VERIFY_TOKEN_ROUTE", "/{token_type}/{token}")
DESTROY_TOKEN_ROUTE = os.getenv("DESTROY_TOKEN_ROUTE", "/{token}")

CONFIRM_DATA_PROJECTION = {
    "_id": 0,
    "email": 1,
    "login": 1
}

EMAIL_CHANGE_TOKEN = "emailChange"


class ErrorCodes(Enum):
    SERVER_ERROR = 25500
    USER_NOT_FOUND = 25501
    DATABASE_ERROR = 25502
    TOKEN_VALIDATOR_ERROR = 25503
    TOKEN_DESTROYER_ERROR = 25504
