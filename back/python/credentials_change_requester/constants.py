import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv('DB_NAME', 'cooking_app')
EMAIL_SYSTEM_API_URL = os.getenv("EMAIL_SYSTEM_API_URL", "http://localhost:8001")
TOKEN_GENERATOR_API_URL = os.getenv("TOKEN_GENERATOR_API_URL", "http://localhost:8002")
MONGO_TIMEOUT = 3

USER_DATA_PROJECTION = {
    "_id": 0,
    "id": 1,
    "email": 1
}


class ErrorCodes(Enum):
    USER_NOT_FOUND = 25700
    UNAUTHORIZED = 25701
    DATABASE_ERROR = 25702
    TOKEN_GENERATION_ERROR = 25703
    EMAIL_SEND_ERROR = 25704
    INVALID_EMAIL = 25705
    SERVER_ERROR = 25706
