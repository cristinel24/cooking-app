import pymongo
from bson import ObjectId

from constants import *


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URL)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_id(self, recipe_id: ObjectId) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            item = self._collection.find_one({"id": recipe_id})
            return item


class UserCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_user_by_id(self, user_id: ObjectId) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            item = self._collection.find_one({"id": user_id})
            del item['id']
            return item

    def add_recipe_to_user(self, user_id: ObjectId, recipe_id: ObjectId):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            self._collection.update_one({"id": user_id}, {"$push": {"savedRecipes": recipe_id}})

    def remove_recipe_from_user(self, user_id: ObjectId, recipe_id: ObjectId):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            self._collection.update_one({"id": user_id}, {"$pull": {"savedRecipes": recipe_id}})
