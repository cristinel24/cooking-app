import os
import re
from enum import Enum
from logging import getLogger

from dotenv import load_dotenv

logger = getLogger("[Recipe Destroyer]")

load_dotenv()
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))
DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
MAX_TIMEOUT_TIME_SECONDS = 3

ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_API_URL")
if ALLERGEN_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'ALLERGEN_MANAGER_API_URL' is not set")
POST_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/"

TAG_MANAGER_API_URL = os.getenv("TAG_MANAGER_API_URL")
if TAG_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'TAG_MANAGER_API_URL' is not set")
POST_TAGS_ROUTE = TAG_MANAGER_API_URL + "/"

RATING_MANAGER_API_URL = os.getenv("RATING_MANAGER_API_URL")
if RATING_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'RATING_MANAGER_API_URL' is not set")
DELETE_RATINGS_ROUTE = RATING_MANAGER_API_URL + "/recipes/{id}/ratings"

IMAGE_STORAGE_API_URL = os.getenv("IMAGE_STORAGE_API_URL")
if IMAGE_STORAGE_API_URL is None:
    logger.warning("Missing IMAGE_STORAGE_API_URL env variable: Will not be able to delete images")

RECIPE_RETRIEVER_API_URL = os.getenv("RECIPE_RETRIEVER_API_URL")
if RECIPE_RETRIEVER_API_URL is None:
    raise ValueError("Environment variable 'RECIPE_RETRIEVER_API_URL' is not set")
RECIPE_RETRIEVE_ROUTE = RECIPE_RETRIEVER_API_URL + "/{recipe_id}"

GATEWAY_API_URL = os.getenv("GATEWAY_API_URL")
if GATEWAY_API_URL is None:
    logger.warning("Missing GATEWAY_API_URL env variable: Will not be able to delete images")

POST_METHOD = "post"
DELETE_METHOD = "delete"
GET_METHOD = "get"

SRC_URL_FROM_IMG_TAG_REGEX = re.compile(rf"<img[^>]*src=[\"']{GATEWAY_API_URL}(?:/[^>]*)*/images/([^\"]*)[\"'][^>]*>")


class UserRoles:
    VERIFIED = 0b1
    ADMIN = 0b10
    PREMIUM = 0b100
    BANNED = 0b1000
    ACTIVE = 0b0


class ErrorCodes(Enum):
    SERVER_ERROR = 26300
    RECIPE_NOT_FOUND = 26301
    FAILED_DESTROY_RECIPE = 26302
    RECIPE_NOT_FOUND_IN_USERS = 26303
    RECIPE_FAILED_TAGS = 26304
    RECIPE_FAILED_ALLERGENS = 26304
    RECIPE_FAILED_RATINGS = 26305
    RECIPE_FAILED_AUTHOR = 26306
    NOT_RESPONSIVE_API = 26307
    RECIPE_FAILED_THUMBNAIL = 26308
    DB_TIMEOUT = 26309
    DB_NON_TIMEOUT = 26310
    UNAUTHENTICATED = 26311
    UNAUTHORIZED = 26312
    USER_ROLES_INVALID_VALUE = 21706
