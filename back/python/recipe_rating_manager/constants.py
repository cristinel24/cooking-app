import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")
RATING_MANAGER_API_URL = os.getenv("RATING_MANAGER_URL", "http://localhost:8001")
MONGO_TIMEOUT = 3

MAX_TIMEOUT_SECONDS = 3

# starts from 26400
class ErrorCodes(Enum):
    DB_ERROR = 26401
    DB_TIMEOUT = 26402
    INVALID_RATING = 26403
    USER_NOT_FOUND = 26404
    RECIPE_NOT_FOUND = 26405
