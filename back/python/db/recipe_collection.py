import pymongo.errors
from pymongo import MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId


class RecipeCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_name(self, recipe_name: str):
        try:
            item = self._collection.find_one({"name": recipe_name})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get recipe by name! - {str(e)}")
        return item

    def get_recipe_by_id(self, recipe_id: str):
        try:
            item = self._collection.find_one({"_id": ObjectId(recipe_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get recipe by id! - {str(e)}")
        return item

    def insert_recipe(self, recipe_data):
        try:
            item = self._collection.insert_one(recipe_data)
            return item.inserted_id
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to insert recipe! - {str(e)}")
        return item

   
if __name__ == "__main__":
    coll = RecipeCollection()
    print(coll.get_recipe_by_id("662b72941e41bc3685bb727b"))
