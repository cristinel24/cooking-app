import pymongo.errors
from pymongo import MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId


class UserCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    # Returns id or none
    def get_user_by_mail(self, mail: str):
        try:
            item = self._collection.find_one({"email": mail})
            if item is None:
                return None
            return item.get("_id")
        except Exception as e:
            raise Exception(f"Failed to get user by mail! - {str(e)}")

    # Returns id or none
    def get_user_by_username(self, username: str):
        try:
            item = self._collection.find_one({"username": username})
            if item is None:
                return None
            return item.get("_id")
        except Exception as e:
            raise Exception(f"Failed to get user by username! - {str(e)}")

    def get_user_by_name(self, user_name: str):
        try:
            item = self._collection.find_one({"name": user_name})
        # TODO: exception handling
        except Exception as e:
            raise Exception(f"Failed to get user by name! - {str(e)}")
        return item

    def get_user_by_id(self, user_id: str):
        try:
            item = self._collection.find_one({"_id": ObjectId(user_id)})
        # TODO: exception handling
        except Exception as e:
            raise Exception(f"Failed to get user by id! - {str(e)}")
        return item

    def insert_user(self, user_data):
        try:
            item = self._collection.insert_one(user_data)
            return item.inserted_id
        # TODO: exception handling
        except Exception as e:
            raise Exception(f"Failed to insert user! - {str(e)}")

    def update_user(self, user_data):
        try:
            item = self._collection.update_one({"_id": user_data["_id"]}, {"$set": user_data})
            return item.upserted_id
        except Exception as e:
            raise Exception(f"Failed to update user! - {str(e)}")


# if __name__ == "__main__":
#     coll = UserCollection()
#     print(coll.get_user_by_mail("ionut.dawfawf@gmail.com"))
#     print(coll.get_user_by_username("ionut.calin"))
