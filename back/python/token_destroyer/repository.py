import os
from datetime import datetime
import pymongo.errors
from pymongo import MongoClient
from bson import ObjectId
from constants import ErrorCodes


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))


class ExpiringTokenCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.expiring_token

    def get_expiring_token(self, value: str, token_type: str | None = None) -> dict:
        try:
            find_query = {
                "value": value
            }
            if token_type is not None:
                find_query["type"] = token_type
            item = self._collection.find_one(find_query)
        except pymongo.errors.PyMongoError as e:
            raise Exception(ErrorCodes.FAILED_TO_GET_TOKEN)
        return item

    def remove_token(self, token_id: ObjectId):
        try:
            result = self._collection.delete_one({"_id": token_id})
            if result.deleted_count == 0:
                raise Exception(ErrorCodes.NO_TOKENS_REMOVED)
        except pymongo.errors.PyMongoError as e:
            raise Exception(ErrorCodes.FAILED_TO_REMOVE_TOKEN)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def update_user_field(self, user_id: str, field: str, value: str):
        """
        update only for sessions and login.changeToken fields in user
        """
        try:
            if field == "sessions":
                updated_items = self._collection.update_one({"id": user_id}, {"$pull": {field: {"value": value}}})
            else:
                updated_items = self._collection.update_one({"id": user_id}, {"$set": {field: None}})
            if updated_items.matched_count == 0:
                raise Exception(ErrorCodes.NO_USERS_MATCHED)
        except pymongo.errors.PyMongoError as e:
            raise Exception(ErrorCodes.FAILED_TO_UPDATE_USER)

