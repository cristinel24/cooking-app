import os

import pymongo
from constants import Errors, MAX_TIMEOUT_SECONDS, TOKEN_TYPES
from pymongo import MongoClient, errors

from exceptions import TokenException


class TokenCollection:
    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token(self, value: str, token_type: str | None = None) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                if token_type is not None and token_type not in TOKEN_TYPES:
                    raise TokenException(Errors.INVALID_TYPE)
                find_query = {
                    "value": value
                }
                if token_type is not None:
                    find_query["tokenType"] = token_type
                item = self._collection.find_one(find_query)
                return item
            except TokenException as e:
                raise e
            except pymongo.errors.ExecutionTimeout:
                raise TokenException(Errors.DB_TIMEOUT)
            except pymongo.errors.PyMongoError:
                raise TokenException(Errors.DB_ERROR)

