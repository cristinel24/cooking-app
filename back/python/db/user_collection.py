from pymongo import errors, MongoClient

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
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get user by mail! - {str(e)}")

    def get_user_by_username(self, username: str) -> dict:
        try:
            item = self._collection.find_one({"username": username})
            return item
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get user by username! - {str(e)}")


    def get_user_by_name(self, user_name: str) -> dict:
        try:
            item = self._collection.find_one({"name": user_name})
        # TODO: exception handling
        except errors.PyMongoError  as e:
            raise Exception(f"Failed to get user by name! - {str(e)}")
        return item

    def get_user_by_id(self, user_id: str) -> dict:
        try:
            item = self._collection.find_one({"_id": ObjectId(user_id)})
        # TODO: exception handling
        except errors.PyMongoError  as e:
            raise Exception(f"Failed to get user by id! - {str(e)}")
        return item

    def insert_user(self, user_data) -> str:
        """
        insert a user into the db and returns the id of the newly inserted user
        :param user_data
        :return: id of the newly inserted user, as str (must be manually cast to ObjectId)
        """
        try:
            item = self._collection.insert_one(user_data)
            return str(item.inserted_id)
        except errors.PyMongoError as e:
            raise Exception(f"Failed to insert user! - {str(e)}")

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
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update user! - {str(e)}")

    def get_user_id_by_name(self, user_name: str) -> ObjectId:
        try:
            return self._collection.find_one(
                {"name": user_name},
                {"_id": 1}
            )["_id"]
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get user id by name! - {str(e)}")

    def get_user_name_by_id(self, user_id: ObjectId) -> str:
        try:
            return self._collection.find_one(
                {"_id": user_id},
                {
                    "name": 1,
                    "_id": 0
                }
            )["name"]
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get user name by id! - {str(e)}")

    def get_user_profile_by_name(self, user_name: str) -> dict:
        try:
            return self._collection.find_one(
                {"name": user_name},
                {
                    "_id": 0,
                    "username": 1,
                    "displayName": 1,
                    "icon": 1,
                    "description": 1,
                    "allergens": 1,
                    "tags": 1,
                    "ratingSum": 1,
                    "ratingCount": 1,
                }
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get user profile! - {str(e)}")

    def update_user_by_name(self, user_name: str, updated_fields: dict) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$set": updated_fields}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update user by name! - {str(e)}")

    def update_saved_recipes_by_name(self, user_name: str, recipe_id: ObjectId) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$push": {"savedRecipes": recipe_id}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update saved recipes! - {str(e)}")

    def delete_saved_recipe_by_name(self, user_name: str, recipe_id: ObjectId) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$pull": {"savedRecipes": recipe_id}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete saved recipe! - {str(e)}")

    def update_search_history_by_name(self, user_name: str, search: str) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$push": {"searchHistory": search}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update search history! - {str(e)}")

    def delete_search_history_by_name(self, user_name: str) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$set": {"searchHistory": []}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete search history! - {str(e)}")

    def get_search_history_by_name(self, user_name: str) -> list:
        try:
            return self._collection.find_one(
                {"name": user_name},
                {"_id": 0, "searchHistory": 1}
            )["searchHistory"]
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get search history! - {str(e)}")

    def update_message_history_by_name(self, user_name: str, message: str) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$push": {"messageHistory": message}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update message history! - {str(e)}")

    def get_message_history_by_name(self, user_name: str) -> list:
        try:
            return self._collection.find_one(
                {"name": user_name},
                {"_id": 0, "messageHistory": 1}
            )["messageHistory"]
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get message history! - {str(e)}")

    def delete_message_history_by_name(self, user_name: str) -> None:
        try:
            self._collection.update_one(
                {"name": user_name},
                {"$set": {"messageHistory": []}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete message history! - {str(e)}")
