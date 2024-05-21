import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 2345))
HOST = os.getenv("HOST", "127.0.0.1")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
DB_NAME = os.getenv("DB_NAME", "cooking_app")


RATING_MANAGER_API_URL = os.getenv("RATING_MANAGER_API_URL", "http://localhost:8001")
USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://localhost:8002")
ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://localhost:8003")

MAX_TIMEOUT_SECONDS = 3

# error codes start from 26400
class ErrorCodes(Enum):
    DB_ERROR = 26401
    DB_TIMEOUT = 26402
    INVALID_RATING = 26403
    USER_NOT_FOUND = 26404
    RECIPE_NOT_FOUND = 26405
    NOT_RESPONSIVE_RATING_MANAGER = 26406
    INTERNAL_SERVER_ERROR = 26407
    UNKNOWN_ERROR = 26508

