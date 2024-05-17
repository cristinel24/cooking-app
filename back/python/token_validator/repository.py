import os

import pymongo
from constants import Errors, MAX_TIMEOUT_SECONDS, TOKEN_TYPES
from pymongo import MongoClient, errors

from exceptions import TokenException


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.user

    def find_user_roles(self, user_id: str):
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user_roles = self._collection.update_one({"id": user_id}, {"roles": 1})
                return user_roles
            except pymongo.errors.ExecutionTimeout:
                raise TokenException(Errors.DB_TIMEOUT)
            except pymongo.errors.PyMongoError as e:
                raise TokenException(Errors.DB_ERROR)


class TokenCollection:
    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token(self, value: str, token_type: str | None = None) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
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

