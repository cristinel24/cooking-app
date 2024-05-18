import pymongo
from pymongo import errors
from fastapi import status
from constants import MONGO_URL, MAX_TIMEOUT_TIME_SECONDS, ErrorCodes
import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URL)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_id(self, recipe_id: str, projection_arg: dict) -> dict:
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                item = self._collection.find_one({"id": recipe_id}, projection=projection_arg)
                if item is None:
                    raise exceptions.RecipeException(status.HTTP_404_NOT_FOUND, ErrorCodes.NONEXISTENT_RECIPE)
                return item
        except errors.PyMongoError as e:
            print(e)
            raise exceptions.RecipeException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.SERVER_ERROR)

