import pymongo.errors
from pymongo import MongoClient

from mongo_collection import MongoCollection
from bson import ObjectId


class RatingCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    
    def get_rating_by_author_id(self, author_id: str):
        try:
            item = self._collection.find_one({"authorId": ObjectId(author_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating by author id! - {str(e)}")
        return item

    def get_rating_by_name(self, param_name: str):
        try:
            item = self._collection.find_one({"name": param_name})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating column from Rating table ! - {str(e)}")
        return item

    def get_rating_by_recipe_id(self, recipe_id: str):
        try:
            item = self._collection.find_one({"recipeId": ObjectId(recipe_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating by recipe! - {str(e)}")
        return item
