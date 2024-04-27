from bson import ObjectId
from pymongo import MongoClient

from db.mongo_collection import MongoCollection


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._db = self._connection.cooking_app
        self._collection = self._db.recipe

    def find_recipe_by_id(self, recipe_id: str) -> dict:
        recipe = self._collection.find_one({"_id": ObjectId(recipe_id)})
        return recipe

    def find_recipe_by_name(self, recipe_name: str) -> dict:
        return self._collection.find_one({"name": recipe_name})

    def find_recipe_id_by_name(self, recipe_name: str) -> ObjectId:
        return self._collection.find_one(
            {"name": recipe_name},
            {"_id": 1}
        )["_id"]

    def find_recipe_card_by_id(self, recipe_id: str) -> dict:
        return self._collection.find_one(
            {"_id": ObjectId(recipe_id)},
            {
                "_id": 0,
                "name": 1,
                "description": 1,
                "authorId": 1,
                "title": 1,
                "prepTime": 1,
                "allergens": 1,
                "tags": 1
             }
        )
