import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")
ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_URL", "http://localhost:8001")
MONGO_TIMEOUT = 3


class ErrorCodes(Enum):
    USER_NOT_FOUND = 21800
    DATABASE_ERROR = 21801
    SERVER_ERROR = 21802
    INVALID_DATA = 21803
    UNAUTHORIZED = 21804
    ADD_ALLERGEN_ERROR = 21805
    REMOVE_ALLERGEN_ERROR = 21806
