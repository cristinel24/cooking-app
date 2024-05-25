from pymongo import MongoClient, errors, timeout
from constants import MAX_TIMEOUT_TIME_SECONDS, MONGO_URI, ErrorCodes, DB_NAME

class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(MONGO_URI)

class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe
        
    def ping_recipe(self, recipe_id:str):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                if self._collection.find_one({id: recipe_id}, {"_id": 0, "id": 1}) is not None:
                    return True
        except errors.PyMongoError as e:
            return ErrorCodes.FAILED_DESTROY_RECIPE
        return False
   
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
                details_rating = {}
                recipe = self._collection.find_one({"id": recipe_id}, {"tags": 1, "allergens": 1, "ratings": 1, "authorId": 1, "thumbnail": 1})
                details_rating["tags"] = recipe.get("tags", [])
                details_rating["allergens"] = recipe.get("allergens", [])
                details_rating["ratings"] = recipe.get("ratings", [])
                details_rating["authorId"] = recipe.get("authorId", "")
                details_rating["thumbnail"] = recipe.get("thumbnail", "")

            except errors.PyMongoError as e:
                return ErrorCodes.RECIPE_NOT_FOUND
            return details_rating
            
    
class UserCollection(MongoCollection):
     def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user
    
     def delete_recipe_from_users(self, recipe_id: str, user_id: str) -> None:
        with timeout(MAX_TIMEOUT_TIME_SECONDS):    
            try:
                result = self._collection.update_many(
                    {"id": user_id},
                    {"$pull": {"recipes": recipe_id}},
                )
                if result.modified_count == 0:
                    return ErrorCodes.RECIPE_NOT_FOUND_IN_USERS
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_DESTROY_RECIPE
            
class RatingCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).rating
    def get_rating_data(self, rating_id: str):
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                details={}
                rating = self._collection.find_one({"id": rating_id}, {"authorId": 1, "rating": 1, "description": 1, "parentType": 1})
                details["authorId"] = rating.get("authorId", "")
                details["rating"] = rating.get("rating", 0)
                details["description"] = rating.get("description", "")
                details["parentType"] = rating.get("parentType", "")

            except errors.PyMongoError as e:
                return ErrorCodes.RATING_NOT_FOUND
            return details
