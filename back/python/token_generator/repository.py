from datetime import datetime, timezone

import pymongo
from constants import *
from exceptions import TokenException, UserException
from pymongo import MongoClient
from fastapi import status


class MongoCollection:
    def __init__(self):
        self._connection = MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).user

    def exists_user(self, user_id: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_SECONDS):
                return self._collection.find_one({"id": user_id}) is not None
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise TokenException(status.HTTP_504_GATEWAY_TIMEOUT, Errors.DB_TIMEOUT)
            else:
                raise TokenException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DB_ERROR)


class TokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def insert_token(self, value: str, user_id: str, token_type: str) -> dict:
        try:
            with pymongo.timeout(MAX_TIMEOUT_SECONDS):
                token = {
                    "value": value,
                    "createdAt": datetime.now(timezone.utc),
                    "userId": user_id,
                    "tokenType": token_type
                }

                if token_type != "session":
                    self._collection.update_one(
                        {"userId": user_id, "tokenType": {"$ne": "session"}},
                        {"$set": token},
                        upsert=True,
                    )
                else:
                    self._collection.insert_one(token)
                    token.pop("_id")

                token.pop("createdAt")

                return token
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise TokenException(status.HTTP_504_GATEWAY_TIMEOUT, Errors.DB_TIMEOUT)
            else:
                raise TokenException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DB_ERROR)

    def exists_token(self, value: str) -> bool:
        try:
            with pymongo.timeout(MAX_TIMEOUT_SECONDS):
                return self._collection.find_one({"value": value}) is not None
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise TokenException(status.HTTP_504_GATEWAY_TIMEOUT, Errors.DB_TIMEOUT)
            else:
                raise TokenException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DB_ERROR)
