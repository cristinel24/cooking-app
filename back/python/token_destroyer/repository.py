import os
from datetime import datetime
import pymongo.errors
from pymongo import MongoClient
from bson import ObjectId


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
            raise Exception(f"Failed to get token! - {str(e)}")
        return item

    def remove_token(self, token_id: ObjectId):
        try:
            result = self._collection.delete_one({"_id": token_id})
            if result.deleted_count == 0:
                raise Exception(f"No tokens were removed")
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to remove token! - {str(e)}")


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_user_by_id(self, user_id: str) -> dict:
        try:
            item = self._collection.find_one({"id": user_id})
        # TODO: exception handling
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get user by id! - {str(e)}")
        return item

    def update_user(self, user_data):
        """
        update a user and return the id of the user
        :param user_data
        :return: id of the newly updated user, as str (must be manually cast to ObjectId)
        """
        try:
            updated_items = self._collection.update_one({"_id": user_data["_id"]}, {"$set": user_data})
            if updated_items.matched_count == 0:
                raise Exception("No users matched")
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to update user! - {str(e)}")

