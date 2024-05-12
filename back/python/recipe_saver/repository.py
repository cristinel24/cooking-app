import pymongo
from constants import *
from recipe_saver import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URL)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_id(self, recipe_id: str) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            item = self._collection.find_one({"id": recipe_id})
            return item


class UserCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def get_user_by_id(self, user_id: str) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            item = self._collection.find_one({"id": user_id})
            del item['id']
            return item

    def add_recipe_to_user(self, user_id: str, recipe_id: str):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            updated_count = self._collection.update_one({"id": user_id}, {"$push": {"savedRecipes": recipe_id}})
            if updated_count == 0:
                raise exceptions.RecipeSaverException(ErrorCodes.NONEXISTENT_USER.value)


    def remove_recipe_from_user(self, user_id: str, recipe_id: str):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            self._collection.update_one({"id": user_id}, {"$pull": {"savedRecipes": recipe_id}})
