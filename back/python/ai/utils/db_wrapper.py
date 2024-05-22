import os
from pymongo import MongoClient
from bson.objectid import ObjectId

from utils.constants import DB_NAME, MONGO_URI


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
        self._connection = MongoClient(MONGO_URI)

    @property
    def _admin_database(self):
        return self._connection.admin

    @property
    def _recipe_collection(self):
        return self._connection.get_database(DB_NAME).recipe

    @property
    def _user_collection(self):
        return self._connection.get_database(DB_NAME).user

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
