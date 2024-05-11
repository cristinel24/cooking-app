import pymongo
from bson import ObjectId

from constants import MONGO_URL, MAX_TIMEOUT_TIME_SECONDS


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URL)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_id(self, recipe_id: ObjectId) -> dict:
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            item = self._collection.find_one({"_id": recipe_id})
            del item['_id']
            return item
