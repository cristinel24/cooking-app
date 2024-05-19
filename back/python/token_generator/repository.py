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
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                return self._collection.find_one({"id": user_id}) is not None
            except pymongo.errors.PyMongoError:
                raise UserException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DATABASE_ERROR)


class TokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def insert_token(self, value: str, user_id: str, token_type: str) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                token = {
                    "value": value,
                    "createdAt": datetime.now(timezone.utc),
                    "userId": user_id,
                    "tokenType": token_type
                }

                self._collection.insert_one(token)

                token.pop("_id")
                token.pop("createdAt")

                return token
            except pymongo.errors.PyMongoError:
                raise TokenException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DATABASE_ERROR)

    def exists_token(self, value: str) -> bool:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                return self._collection.find_one({"value": value}) is not None
            except pymongo.errors.PyMongoError:
                raise TokenException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DATABASE_ERROR)
