import os
from enum import Enum

PORT = os.getenv("PORT", 8000)
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")
MONGO_TIMEOUT = 3


class ErrorCodes(Enum):
    USER_NOT_FOUND = 21800
    DATABASE_ERROR = 21801
    SERVER_ERROR = 21802
