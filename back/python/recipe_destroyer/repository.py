import os
from pymongo import MongoClient, errors, timeout
from constants import MAX_TIMEOUT_TIME_SECONDS, ErrorCodes

class RecipeCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI"))
        self._collection = self._connection['cooking_app']['recipe']
        
    def delete_recipe(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                result = self._collection.delete_one({"id": recipe_id})
                if result.deleted_count == 0:
                    return ErrorCodes.RECIPE_NOT_FOUND
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_DESTROY_RECIPE
            
    
    def get_recipe_details(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, {"tags": 1, "allergens": 1, "ratings": 1, "authorId": 1, "thumbnail":1})
                if recipe is None:
                    return {
                        "tags": ErrorCodes.RECIPE_NOT_FOUND,
                        "allergens": ErrorCodes.RECIPE_NOT_FOUND,
                        "ratings": ErrorCodes.RECIPE_NOT_FOUND,
                        "authorId": ErrorCodes.RECIPE_NOT_FOUND,
                        "thumbnail": ErrorCodes.RECIPE_NOT_THUMBNAIL
                    }
                return {
                    "tags": recipe.get("tags", []),
                    "allergens": recipe.get("allergens", []),
                    "ratings": recipe.get("ratings", []),
                    "authorId": recipe.get("authorId", ""),
                    "thumbnail": recipe.get("thumbnail", "")
                }
            except errors.PyMongoError as e:
                return {
                    "tags": ErrorCodes.RECIPE_NOT_TAGS,
                    "allergens": ErrorCodes.RECIPE_NOT_ALLERGENS,
                    "ratings": ErrorCodes.RECIPE_NOT_RATINGS,
                    "authorId": ErrorCodes.RECIPE_NOT_AUTHOR,
                    "thumbnail": ErrorCodes.RECIPE_NOT_THUMBNAIL
                }
            
    
class UserCollection:
     def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection['cooking_app']['user']
    
     def delete_recipe_from_users(self, recipe_id: str, user_id: str) -> None:
        with timeout(MAX_TIMEOUT_TIME_SECONDS):    
            try:
                result = self._collection.update_many(
                    {"id": user_id},
                    {"$pull": {"recipes": recipe_id}}
                )
                if result.modified_count == 0:
                    return ErrorCodes.RECIPE_NOT_FOUND_IN_USERS
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_DESTROY_RECIPE
            
        