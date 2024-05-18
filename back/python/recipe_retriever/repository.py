import exceptions
import pymongo
from constants import DB_NAME, MAX_TIMEOUT_TIME_SECONDS, MONGO_URI, ErrorCodes
from fastapi import status
from pymongo import errors


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URI)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe

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

