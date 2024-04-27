import os
import sys

import pymongo.errors
from pymongo import MongoClient

from db.mongo_collection import MongoCollection
from bson import ObjectId
from datetime import datetime


class RecipeCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_name(self, recipe_name: str):
        try:
            item = self._collection.find_one({"name": recipe_name})
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get recipe by name! - {str(e)}")
        return item

    def get_recipe_by_id(self, recipe_id: str):
        try:
            item = self._collection.find_one({"_id": ObjectId(recipe_id)})
        except pymongo.errors.Any as e:
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
                    "description": params["description"],
                    "prepTime": params["prepTime"],
                    "steps": params["steps"],
                    "ingredients": params["ingredients"],
                    "allergens": params["allergens"],
                    "tags": params["tags"],
                    "tokens": [],
                    "ratings": []
                }
            )
            return item.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert recipe! - {str(e)}")

    def delete_recipe_by_id(self, recipe_id: str):
        try:
            self._collection.delete_one({"_id": ObjectId(recipe_id)})
        except Exception as e:
            raise Exception(f"Failed to delete recipe! - {str(e)}")

    def delete_recipe_by_name(self, recipe_name: str):
        try:
            self._collection.delete_one({"name": recipe_name})
        except Exception as e:
            raise Exception(f"Failed to delete recipe! - {str(e)}")

    def update_recipe_by_name(self, recipe_name: str, update_data: dict):
        try:
            update_dict = {"$set": update_data}
            update_dict["$set"]["updatedAt"] = datetime.utcnow()
            result = self._collection.update_one({"name": recipe_name}, update_dict)
            return result.raw_result
        except Exception as e:
            raise Exception(f"Failed to update recipe by name! - {str(e)}")

    def update_recipe_by_id(self, recipe_id: str, update_data: dict):
        try:
            update_dict = {"$set": update_data}
            update_dict["$set"]["updatedAt"] = datetime.utcnow()
            result = self._collection.update_one({"name": ObjectId(recipe_id)}, update_dict)
            return result
        except Exception as e:
            raise Exception(f"Failed to update recipe by id! - {str(e)}")

    def add_tokens_by_name(self, recipe_name: str, recipe_tokens: list[str]):
        try:
            update_result = self._collection.update_one(
                {"name": recipe_name},
                {"$addToSet": {"tokens": {"$each": recipe_tokens}}}
            )
            return update_result
        except Exception as e:
            raise Exception(f"Failed to add tokens to recipe tags! - {str(e)}")

    def add_tokens_by_id(self, recipe_id: str, recipe_tokens: list[str]):
        try:
            update_result = self._collection.update_one(
                {"_id": ObjectId(recipe_id)},
                {"$addToSet": {"tokens": {"$each": recipe_tokens}}}
            )
            return update_result
        except Exception as e:
            raise Exception(f"Failed to add tokens to recipe tags! - {str(e)}")
