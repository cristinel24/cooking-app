import pymongo
from constants import *
from fastapi import status

import exceptions


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def add_recipe_to_user(self, user_id: str, recipe_id: str):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.update_one(
                {"id": user_id},
                [
                    {
                        "$set": {
                            "savedRecipes": {
                                "$cond": {
                                    "if": {"$in": [recipe_id, "$savedRecipes"]},
                                    "then": "$savedRecipes",
                                    "else": {"$concatArrays": [[recipe_id], "$savedRecipes"]}
                                }
                            }
                        }
                    }
                ]
            )
            if result.matched_count == 0:
                raise exceptions.RecipeSaverException(status.HTTP_404_NOT_FOUND, ErrorCodes.NONEXISTENT_USER.value)

    def get_saved_recipes(self, user_id: str, start: int, count: int) -> dict:

        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            return self._collection.find_one(
                {"id": user_id},
                {
                    "_id": 0, 
                    "savedRecipes": {"$slice": [start, start + count]}, 
                    "total": {"$size": "$savedRecipes"}
                }
            )

    def remove_recipe_from_saved(self, user_id: str, recipe_id: str):
        with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
            result = self._collection.update_one({"id": user_id}, {"$pull": {"savedRecipes": recipe_id}})
            if result.matched_count == 0:
                raise exceptions.RecipeSaverException(status.HTTP_404_NOT_FOUND, ErrorCodes.NONEXISTENT_USER.value)
            if result.modified_count == 0:
                raise exceptions.RecipeSaverException(status.HTTP_404_NOT_FOUND, ErrorCodes.RECIPE_NOT_SAVED.value)
