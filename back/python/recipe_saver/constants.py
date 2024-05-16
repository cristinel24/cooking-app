import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8001))
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
MAX_TIMEOUT_TIME_SECONDS = 3


class ErrorCodes(Enum):
    SERVER_ERROR = 21500
    NONEXISTENT_USER = 21501
    NONEXISTENT_RECIPE = 21502
    RECIPE_ALREADY_SAVED = 21503
    RECIPE_NOT_SAVED = 21504
    WRONG_USER_ID = 21505
