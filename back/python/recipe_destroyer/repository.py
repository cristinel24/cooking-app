import os
from pymongo import MongoClient, errors, timeout
from constants import MAX_TIMEOUT_TIME_SECONDS, ErrorCodes

class RecipeCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection['cooking_app']['recipe']
        
    def delete_recipe_mongo(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                result = self._collection.delete_one({"id": recipe_id})
                if result.deleted_count == 0:
                    return ErrorCodes.RECIPE_NOT_FOUND
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_DESTROY_RECIPE
            return 0
    
    def get_tags_from_recipe(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, {"tags": 1})
                if recipe is None:
                    return ErrorCodes.RECIPE_NOT_FOUND
                return recipe.get("tags", [])
            except errors.PyMongoError as e:
                return ErrorCodes.RECIPE_NOT_TAGS
            return 0
    
    def get_allergens_from_recipe(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, {"allergens": 1})
                if recipe is None:
                    return ErrorCodes.RECIPE_NOT_FOUND
                return recipe.get("allergens", [])
            except errors.PyMongoError as e:
                 return ErrorCodes.RECIPE_NOT_ALLERGENS
            return 0
            
    def get_ratings_from_recipe(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, {"ratings": 1})
                if recipe is None:
                    return ErrorCodes.RECIPE_NOT_FOUND
                return recipe.get("ratings", [])
            except errors.PyMongoError as e:
                return ErrorCodes.RECIPE_NOT_RATINGS
            return 0
    
    def get_author_from_recipe(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, {"authorId": 1})
                if recipe is None:
                    return ErrorCodes.RECIPE_NOT_FOUND
                return recipe.get("authorId", "")
            except errors.PyMongoError as e:
                return ErrorCodes.RECIPE_NOT_AUTHOR
            return 0
    
    def get_thumbnail_from_recipe(self, recipe_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                recipe = self._collection.find_one({"id": recipe_id}, {"thumbnail": 1})
                if recipe is None:
                    return ErrorCodes.RECIPE_NOT_FOUND
                return recipe.get("thumbnail", "")
            except errors.PyMongoError as e:
                return ErrorCodes.RECIPE_NOT_THUMBNAIL    
            return 0    
    
    
   
class UserCollection:
     def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection['cooking_app']['user']
    
     def delete_recipe_from_users_mongo(self, recipe_id: str, user_id: str) -> None:
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
            return 0