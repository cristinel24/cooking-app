from pymongo import errors, DeleteOne, MongoClient

from generic.recipe.schemas import RecipeData
from db.mongo_collection import MongoCollection
from db import user_collection
from bson import ObjectId
from datetime import datetime


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_name(self, recipe_name: str) -> dict:
        try:
            item = self._collection.find_one({"name": recipe_name})
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get recipe by name! - {str(e)}")
        return item

    def get_recipe_by_id(self, recipe_id: str) -> dict:
        try:
            item = self._collection.find_one({"_id": ObjectId(recipe_id)})
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get recipe by id! - {str(e)}")
        return item

    def insert_recipe(self, params):
        try:
            item = self._collection.insert_one(
                {
                    "updatedAt": datetime.utcnow(),
                    "name": params["name"],
                    "authorId": ObjectId(params["authorId"]),
                    "title": params["title"],
                    "ratingSum": 0,
                    "ratingCount": 0,
                    "description": params["description"],
                    "prepTime": params["prepTime"],
                    "steps": params["steps"],
                    "ingredients": params["ingredients"],
                    "allergens": params["allergens"],
                    "tags": params["tags"],
                    "tokens": [],
                    "ratings": [],
                    "mainImage": "matei.speg"
                }
            )
            return item.inserted_id
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to insert recipe! - {str(e)}")

    def get_recipe_id_by_name(self, recipe_name: str) -> ObjectId:
        try:
            return self._collection.find_one(
                {"name": recipe_name},
                {"_id": 1}
            )["_id"]
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get recipe id by name! - {str(e)}")

    def delete_recipe_by_id(self, recipe_id: str):
        try:
            self._collection.delete_one({"_id": ObjectId(recipe_id)})
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete recipe! - {str(e)}")
        
    def delete_recipe_by_name(self, recipe_name: str):
        try:
            self._collection.delete_one({"name": recipe_name})
        # TODO: exception handling
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete recipe! - {str(e)}")

    def update_recipe_by_name(self, recipe_name: str, update_data: dict):
        try:
            update_dict = {"$set": update_data}
            update_dict["$set"]["updatedAt"] = datetime.utcnow()
            self._collection.update_one({"name": recipe_name}, update_dict)
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update recipe by name! - {str(e)}")

    def update_recipe_by_id(self, recipe_id: str, update_data: dict):
        try:
            update_dict = {"$set": update_data}
            update_dict["$set"]["updatedAt"] = datetime.utcnow()
            self._collection.update_one({"name": ObjectId(recipe_id)}, update_dict)
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update recipe by id! - {str(e)}")

    def add_tokens_by_name(self, recipe_name: str, recipe_tokens: list[str]):
        try:
            self._collection.update_one(
                {"name": recipe_name},
                {"$addToSet": {"tokens": {"$each": recipe_tokens}}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to add tokens to recipe tags! - {str(e)}")

    def add_tokens_by_id(self, recipe_id: str, recipe_tokens: list[str]):
        try:
            self._collection.update_one(
                {"_id": ObjectId(recipe_id)},
                {"$addToSet": {"tokens": {"$each": recipe_tokens}}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to add tokens to recipe tags! - {str(e)}")

    def get_recipe_card_by_id(self, recipe_id: str) -> dict:
        try:
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
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get recipe card! - {str(e)}")



