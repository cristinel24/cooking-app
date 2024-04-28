from pymongo import errors, MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId


class RatingCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.rating

    def get_ratings_by_author_id(self, author_id: str, start: int, limit: int):
        try:
            item = self._collection.find_one({"authorId": ObjectId(author_id)})
            return item
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get rating by author id! - {str(e)}")

    def get_rating_by_name(self, rating_name: str):
        try:
            item = self._collection.find_one({"name": rating_name})
            return item
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get rating column from Rating table ! - {str(e)}")

    def get_ratings_by_recipe_id(self, recipe_id: str, start: int, limit: int):
        try:
            ratings = self._collection.find({"recipeId": ObjectId(recipe_id)}).skip(start).limit(limit)
            if not ratings:
                raise Exception("No ratings found for the provided recipe_id!")
            return ratings
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get ratings by recipe id! - {str(e)}")

    def get_comments_by_rating_id(self, rating_id: str, start: int, limit: int) -> list[str]:
        try:
            items = self._collection.find({"parentId": ObjectId(rating_id)}).skip(start).limit(limit)
            if not items:
                raise Exception("No comments found for the provided rating_id!")
            return items
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get comments by rating id! - {str(e)}")

    def get_rating_by_id(self, rating_id: str) -> dict:
        try:
            item = self._collection.find_one({"_id": ObjectId(rating_id)})
            return item
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get rating by recipe! - {str(e)}")

    def insert_rating(self, rating_data):
        try:
            item = self._collection.insert_one(rating_data)
            return item.inserted_id
        except errors.PyMongoError as e:
            raise Exception(f"Failed to insert rating! - {str(e)}")

    def update_rating(self, rating_id: str, rating_data):
        try:
            result = self._collection.update_one({"_id": ObjectId(rating_id)}, {"$set": rating_data})
            if result.modified_count > 0:
                return rating_id
            else:
                raise Exception(f"No rating was modified with the ID: {rating_id}")
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update rating! - {str(e)}")

    def delete_rating(self, rating_id: str):
        try:
            result = self._collection.delete_one({"_id": ObjectId(rating_id)})
            if result.deleted_count == 0:
                raise Exception(f"No rating was deleted with the ID: {rating_id}")
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete rating! - {str(e)}")
