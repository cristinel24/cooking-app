import pymongo.errors
from pymongo import MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId


class RatingCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.rating

    def get_ratings_by_author_id(self, author_id: str, limit: int):
        try:
            items = self._collection.find({"authorId": ObjectId(author_id)}).limit(limit)
            ratings = [item for item in items]
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get ratings by author id! - {str(e)}")
        return ratings

    def get_rating_by_name(self, rating_name: str):
        try:
            item = self._collection.find_one({"name": rating_name})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating column from Rating table ! - {str(e)}")
        return item

    def get_ratings_by_recipe_id(self, recipe_id: str, limit: int):
        try:
            items = self._collection.find({"recipeId": ObjectId(recipe_id)}).limit(limit)
            ratings = [item for item in items]
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get ratings by recipe id! - {str(e)}")
        return ratings

    def get_rating_by_id(self, rating_id: str):
        try:
            item = self._collection.find_one({"recipeId": ObjectId(rating_id)})
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get rating by recipe! - {str(e)}")
        return item

    def insert_rating(self, rating_data):
        try:
            item = self._collection.insert_one(rating_data)
            return item.inserted_id
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to insert rating! - {str(e)}")

    def insert_rating(self, name: str, updatedAt: datetime, authorId: ObjectId, recipeId: ObjectId, rating: int,
                      description: str, parentId: ObjectId, children: list[ObjectId]) -> ObjectId:
        try:
            rating_data = {
                "name": name,
                "updatedAt": updatedAt,
                "authorId": authorId,
                "recipeId": recipeId,
                "rating": rating,
                "description": description,
                "parentId": parentId,
                "children": children
            }
            item = self._collection.insert_one(rating_data)
            return item.inserted_id
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to insert rating! - {str(e)}")

    def update_rating(self, rating_id: str, rating_data):
        try:
            item = self._collection.update_one({"_id": ObjectId(rating_id)}, {"$set": rating_data})
            return item.modified_count
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to update rating! - {str(e)}")

    def delete_rating(self, rating_id: str):
        try:
            item = self._collection.delete_one({"_id": ObjectId(rating_id)})
            return item.deleted_count
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to delete rating! - {str(e)}")
