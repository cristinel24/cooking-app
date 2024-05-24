import pymongo
from pymongo import MongoClient, errors
from schemas import *
from constants import *
from exceptions import RecipeRatingManagerException


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)

    def get_connection(self) -> MongoClient:
        return self._connection


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def update_user_ratings(self, author_id: str, rating: int):
        if not (1 <= rating <= 5):
            raise RecipeRatingManagerException(ErrorCodes.INVALID_RATING.value, "Invalid rating! Should be a value "
                                                                                "between 1 and 5")

        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one({"id": author_id}, USER_PROJECTION)
                if not user:
                    raise RecipeRatingManagerException(ErrorCodes.USER_NOT_FOUND.value, "User not found")

                # Update ratingSum and ratingCount
                self._collection.update_one(
                    {"id": author_id},
                    {
                        "$inc": {"ratingSum": rating, "ratingCount": 1}
                    }
                )
            except pymongo.errors.PyMongoError:
                raise RecipeRatingManagerException(ErrorCodes.DB_ERROR.value, "Database error!")

    def remove_user_rating(self, author_id: str, rating_value: int):
        if not (1 <= rating_value <= 5):
            raise RecipeRatingManagerException(ErrorCodes.INVALID_RATING.value, "Invalid rating! Should be a value "
                                                                                "between 1 and 5")

        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one({"id": author_id}, USER_PROJECTION)
                if not user:
                    raise RecipeRatingManagerException(ErrorCodes.USER_NOT_FOUND.value, "User not found")

                self._collection.update_one(
                    {"id": author_id},
                    {
                        "$inc": {"ratingSum": -rating_value, "ratingCount": -1}
                    }
                )
            except pymongo.errors.PyMongoError:
                raise RecipeRatingManagerException(ErrorCodes.DB_ERROR.value, "Database error!")


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe

    def update_recipe_ratings(self, recipe_id: str, rating: int):
        if not (1 <= rating <= 5):
            raise RecipeRatingManagerException(ErrorCodes.INVALID_RATING.value, "Invalid rating! Should be a value "
                                                                                "between 1 and 5")

        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, RECIPE_PROJECTION)
                if not recipe:
                    raise RecipeRatingManagerException(ErrorCodes.RECIPE_NOT_FOUND.value, "Recipe not found!")

                self._collection.update_one(
                    {"id": recipe_id},
                    {
                        "$inc": {"ratingSum": rating, "ratingCount": 1}
                    }
                )
            except pymongo.errors.PyMongoError:
                raise RecipeRatingManagerException(ErrorCodes.DB_ERROR.value, "Database error!")

    def remove_recipe_rating(self, recipe_id: str, rating_value: int):
        if not (1 <= rating_value <= 5):
            raise RecipeRatingManagerException(ErrorCodes.INVALID_RATING.value, "Invalid rating! Should be a value "
                                                                                "between 1 and 5")

        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, RECIPE_PROJECTION)
                if not recipe:
                    raise RecipeRatingManagerException(ErrorCodes.RECIPE_NOT_FOUND.value, "Recipe not found")

                self._collection.update_one(
                    {"id": recipe_id},
                    {
                        "$inc": {"ratingSum": -rating_value, "ratingCount": -1}
                    }
                )
            except pymongo.errors.PyMongoError:
                raise RecipeRatingManagerException(ErrorCodes.DB_ERROR.value, "Database error!")
