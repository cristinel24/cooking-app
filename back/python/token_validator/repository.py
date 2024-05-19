from constants import *
from pymongo import MongoClient, errors, timeout

from exceptions import TokenException


class UserCollection:
    def __init__(self):
        self._connection = MongoClient(MONGO_URI)
        self._collection = self._connection.get_database(DB_NAME).user

    def find_user_roles(self, user_id: str) -> dict | None:
        with timeout(MAX_TIMEOUT_SECONDS):
            try:
                user_roles = self._collection.find_one({"id": user_id}, GET_EXPIRING_TOKEN)
                return user_roles
            except errors.ExecutionTimeout:
                raise TokenException(Errors.DB_TIMEOUT)
            except errors.PyMongoError:
                raise TokenException(Errors.DB_ERROR)


class TokenCollection:
    def __init__(self):
        self._connection = MongoClient(MONGO_URI)
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def get_expiring_token(self, token: str, token_type: str | None) -> dict | None:
        with timeout(MAX_TIMEOUT_SECONDS):
            try:
                find_query = {
                    "value": token
                }
                if token_type is not None:
                    find_query["tokenType"] = token_type
                item = self._collection.find_one(find_query)
                return item
            except TokenException as e:
                raise e
            except errors.ExecutionTimeout:
                raise TokenException(Errors.DB_TIMEOUT)
            except errors.PyMongoError:
                raise TokenException(Errors.DB_ERROR)

