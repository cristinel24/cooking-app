import os
from datetime import datetime

import pymongo
from bson import ObjectId
from pymongo import MongoClient, errors
from schemas import expiring_token_projection
from exceptions import TokenException, UserException
from constants import Errors, MAX_TIMEOUT_SECONDS


class MongoCollection:
    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.user

    def insert_token_to_user(self, user_id: str, token_id: str, token_data: dict):
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one({"_id": user_id})
                if user is None:
                    raise UserException(Errors.USER_NOT_FOUND)
                user["sessions"].append({
                    "value": token_data["value"],
                    "tokenType": token_data["tokenType"],
                    "_id": ObjectId(token_id)
                })
                self._collection.update_one({"_id": user_id}, {"$set": user})
            except UserException as e:
                raise e
            except pymongo.errors.PyMongoError as e:
                raise UserException(Errors.DATABASE_ERROR)


user_db = UserCollection()


class TokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.expiring_token

    def insert_token(self, value: str, user_id: str, type_token: str) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                item = self._collection.insert_one({
                    "value": value,
                    "createdAt": datetime.utcnow(),
                    "userId": user_id,
                    "tokenType": type_token
                })
                token_id = item.inserted_id
                user_db.insert_token_to_user(user_id, token_id, {
                    "value": value,
                    "tokenType": type_token
                })
                item = self._collection.find_one({"_id": item.inserted_id}, projection=expiring_token_projection)
                return item
            except UserException as e:
                raise TokenException(e.error_code)
            except pymongo.errors.PyMongoError as e:
                raise TokenException(Errors.DATABASE_ERROR)

    def exists_token(self, value: str) -> bool:
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            return self._collection.find_one({"value": value}) is not None


