import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8000))
DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
MAX_TIMEOUT_TIME_SECONDS = 3

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL")
if ID_GENERATOR_API_URL is None:
    raise ValueError("Environment variable 'ID_GENERATOR_API_URL' is not set")

USER_RETRIEVER_API_URL = os.getenv("USER_RETRIEVER_API_URL")
if USER_RETRIEVER_API_URL is None:
    raise ValueError("Environment variable 'USER_RETRIEVER_API_URL' is not set")

DELETED_FIELD = "«deleted»"

RATING_PROJECTION = {
    "_id": 0,
    "createdAt": {"$toDate": "$_id"},
    "updatedAt": 1,
    "id": 1,
    "authorId": 1,
    "rating": 1,
    "description": 1,
    "parentId": 1,
    "parentType": 1,
    "childrenCount": {"$size": "$children"}
}

POST_METHOD = "post"
PATCH_METHOD = "patch"
DELETE_METHOD = "delete"
GET_METHOD = "get"


class RatingInc(Enum):
    ADD_RATING = 1
    ADJUST_RATING = 0
    REMOVE_RATING = -1


FILTER_DICT = {
    "rating": {"rating": {"$gt": 0}},
    "comment": {"rating": {"$eq": 0}}
}

SORT_DICT = {
    # undefined so far, but prepped
}

DEFAULT_SORT = {"_id": 1}
UPDATE_FIELDS_TO_DELETE = {"$set": {"description": DELETED_FIELD, "authorId": DELETED_FIELD, "rating": 0}}

RECIPE = "recipe"
RATING = "rating"


class ErrorCodes(Enum):
    UNKNOWN = 26400
    DB_TIMEOUT = 26401
    DB_NON_TIMEOUT = 26402
    UNAUTHENTICATED = 26403
    INVALID_RATING_VALUE = 26404
    DB_CONNECTION_FAILURE = 26405
    RATING_NOT_FOUND = 26406
    RATING_ALREADY_EXISTS = 26407
    UNAUTHORIZED = 26408
    RECIPE_AUTHOR_ADDS_SELF_RATING = 26409
    RECIPE_NOT_FOUND = 26410
    INVALID_PARENT_TYPE = 26411
    WRONG_PARENT_TYPE = 26412
    USER_ALREADY_COMMENTED = 26413
    DUPLICATE_GENERATED_ID = 26414
    FAILED_ADDING_CHILD_TO_PARENT = 26415
    MISSING_START_QUERY_PARAM = 26416
    MISSING_COUNT_QUERY_PARAM = 26417
    PARENT_RATING_NOT_FOUND = 26418
    AUTHOR_NOT_FOUND = 26419
