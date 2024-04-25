import os
from pymongo import MongoClient
from bson.objectid import ObjectId


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class DBWrapper:

    def __init__(self):
        self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))

    @property
    def _admin_database(self):
        return self._connection.admin

    @property
    def _recipe_collection(self):
        return self._connection.cooking_app.recipe

    @property
    def _user_collection(self):
        return self._connection.cooking_app.user

    def ping_db(self) -> bool:
        try:
            item = self._admin_database.command("ping")
        except Exception as e:
            raise Exception(f"Failed to ping MongoDB! - {str(e)}")
        return item

    def get_recipe(self, entry_id: str) -> dict:
        try:
            item = self._recipe_collection.find_one({"_id": ObjectId(entry_id)})
        except Exception as e:
            raise Exception(f"Failed to retrieve recipe! - {str(e)}")
        return item

    def get_user_context(self, entry_id: str) -> dict:
        try:
            item = self._user_collection.find_one({"_id": ObjectId(entry_id)})
        except Exception as e:
            raise Exception(f"Failed to retrieve user context! - {str(e)}")
        return item
