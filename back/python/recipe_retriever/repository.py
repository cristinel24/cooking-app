from bson import ObjectId
from pymongo import MongoClient, errors

from constants import MONGO_URL


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)

class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_id(self, recipe_id: ObjectId) -> dict:
        try:
            item = self._collection.find_one({"_id": recipe_id})
            if item:
                del item['_id']
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get recipe by id! - {str(e)}")
        return item
