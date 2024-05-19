import os
from datetime import datetime, timezone

import pymongo
from bson import ObjectId
from constants import *
from exceptions import TokenException, UserException
from pymongo import MongoClient


class MongoCollection:
    def __init__(self):
        self._connection = MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).user

    def insert_token_to_user(self, user_id: str, token_id: str, token_data: dict):
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.update_one({"id": user_id}, {"$push": {"sessions": {
                    "value": token_data["value"],
                    "tokenType": token_data["tokenType"],
                    "_id": ObjectId(token_id)
                }}})
                if user.matched_count == 0:
                    raise UserException(Errors.USER_NOT_FOUND)
            except UserException as e:
                raise e
            except pymongo.errors.PyMongoError as e:
                raise UserException(Errors.DATABASE_ERROR)


user_db = UserCollection()


class TokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).expiring_token

    def insert_token(self, value: str, user_id: str, type_token: str) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                time = datetime.now(timezone.utc)
                item = self._collection.insert_one({
                    "value": value,
                    "createdAt": time,
                    "userId": user_id,
                    "tokenType": type_token
                })
                token_id = item.inserted_id
                user_db.insert_token_to_user(user_id, token_id, {
                    "value": value,
                    "tokenType": type_token
                })
                return {
                    "value": value,
                    "createdAt": time,
                    "userId": user_id,
                    "tokenType": type_token
                }
            except UserException as e:
                raise TokenException(e.error_code)
            except pymongo.errors.PyMongoError as e:
                raise TokenException(Errors.DATABASE_ERROR)

    def exists_token(self, value: str) -> bool:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            return self._collection.find_one({"value": value}) is not None


