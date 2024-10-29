import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8030))
HOST = os.getenv("HOST_URL", "localhost")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
MONGO_TIMEOUT = 3

RECIPE_RETRIEVER_API_URL = os.getenv("RECIPE_RETRIEVER_API_URL", "http://localhost:8001")
if RECIPE_RETRIEVER_API_URL is None:
    raise ValueError("Environment variable 'RECIPE_RETRIEVER_API_URL' is not set")

USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL", "http://localhost:8000")
if USER_RETRIEVER_API_URL is None:
    raise ValueError("Environment variable 'USER_RETRIEVER_API_URL' is not set")

RATING_MANAGER_API_URL = os.getenv("RATING_MANAGER_API_URL", "http://localhost:8002")
if RATING_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'RATING_MANAGER_API_URL' is not set")
DB_NAME = os.getenv("DB_NAME", 'cooking_app')


POST_METHOD = "post"
PATCH_METHOD = "patch"
DELETE_METHOD = "delete"
GET_METHOD = "get"


class ErrorCodes(Enum):
    UNAUTHORIZED = 36600
    UNAUTHENTICATED = 36601
    REPORT_NOT_FOUND = 36602
    INVALID_REPORT_TYPE = 36603
    INVALID_FILTER = 36604
    DATABASE_TIMEOUT = 36605
    DATABASE_ERROR = 36606
