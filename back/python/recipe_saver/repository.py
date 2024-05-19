import pymongo
from constants import *
from fastapi import status

from recipe_saver import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def add_recipe_to_user(self, user_id: str, recipe_id: str):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.update_one(
                {"id": user_id},
                {"$addToSet": {"savedRecipes": recipe_id}}
            )
            if result.matched_count == 0:
                raise exceptions.RecipeSaverException(status.HTTP_404_NOT_FOUND, ErrorCodes.NONEXISTENT_USER.value)

    def remove_recipe_from_saved(self, user_id: str, recipe_id: str):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.update_one({"id": user_id}, {"$pull": {"savedRecipes": recipe_id}})
            if result.matched_count == 0:
                raise exceptions.RecipeSaverException(status.HTTP_404_NOT_FOUND, ErrorCodes.NONEXISTENT_USER.value)
            if result.updated_count == 0:
                raise exceptions.RecipeSaverException(status.HTTP_404_NOT_FOUND, ErrorCodes.RECIPE_NOT_SAVED.value)
