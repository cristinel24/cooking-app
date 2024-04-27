from pymongo import MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId


class UserCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_user_by_mail(self, mail: str) -> dict:
        try:
            item = self._collection.find_one({"email": mail})
            return item
        except Exception as e:
            raise Exception(f"Failed to get user by mail! - {str(e)}")

    def get_user_by_username(self, username: str) -> dict:
        try:
            item = self._collection.find_one({"username": username})
            return item
        except Exception as e:
            raise Exception(f"Failed to get user by username! - {str(e)}")

    def get_user_by_name(self, user_name: str) -> dict:
        try:
            item = self._collection.find_one({"name": user_name})
        except Exception as e:
            raise Exception(f"Failed to get user by name! - {str(e)}")
        return item

    def get_user_by_id(self, user_id: str) -> dict:
        try:
            item = self._collection.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            raise Exception(f"Failed to get user by id! - {str(e)}")
        return item

    def insert_user(self, user_data) -> int:
        """
        insert a user into the db and returns the id of the newly inserted user
        :param user_data
        :return: id of the newly inserted user, as int (must be manually cast to ObjectId)
        """
        try:
            item = self._collection.insert_one(user_data)
            return item.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert user! - {str(e)}")

    def update_user(self, user_data) -> int:
        """
        update a user and return the id of the user
        :param user_data
        :return: id of the newly updated user, as int (must be manually cast to ObjectId)
        """
        try:
            item = self._collection.update_one({"_id": user_data["_id"]}, {"$set": user_data})
            return item.upserted_id
        except Exception as e:
            raise Exception(f"Failed to update user! - {str(e)}")


# if __name__ == "__main__":
#     coll = UserCollection()
#     print(coll.get_user_by_mail("ionut.dawfawf@gmail.com"))
#     print(coll.get_user_by_username("ionut.calin"))
