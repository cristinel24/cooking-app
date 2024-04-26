import pymongo.errors
from pymongo import MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId


class UserCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_user_by_name(self, user_name: str):
        try:
            item = self._collection.find_one({"name": user_name})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get user by name! - {str(e)}")
        return item

    def get_user_by_id(self, user_id: str):
        try:
            item = self._collection.find_one({"_id": ObjectId(user_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get user by id! - {str(e)}")
        return item

    def insert_user(self, user_data):
        try:
            item = self._collection.insert_one(user_data)
            return item.inserted_id
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to insert user! - {str(e)}")
        return item


if __name__ == "__main__":
   coll = UserCollection()
   print(coll.get_user_by_id("662b72721e41bc3685bb71d1"))
