import os
import sys
from typing import List

# to import paths with vscode (pycharm makes this automatically)
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pymongo.errors
from pymongo import DeleteOne, MongoClient

from generic.recipe.schemas import RecipeData
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
        # TODO: exception handling
        except pymongo.errors.Any as e:
            raise Exception(f"Failed to get recipe by name! - {str(e)}")
        return item

    def get_recipe_by_id(self, recipe_id: str):
        try:
            item = self._collection.find_one({"_id": ObjectId(recipe_id)})
        # TODO: exception handling
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
        # TODO: exception handling
        except Exception as e:
            raise Exception(f"Failed to insert recipe! - {str(e)}")

    def delete_recipe_by_id(self, recipe_id: str):
        try:
            self._collection.delete_one({"_id": ObjectId(recipe_id)})
        # TODO: exception handling
        except Exception as e:
            raise Exception(f"Failed to delete recipe! - {str(e)}")

    def delete_recipe_by_name(self, recipe_name: str):
        try:
            self._collection.delete_one({"name": recipe_name})
        # TODO: exception handling
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
            result = self._collection.update_one({"name": recipe_id}, update_dict)
            return result
        except Exception as e:
            raise Exception(f"Failed to update recipe by id! - {str(e)}")

    def add_tokens_by_name(self, recipe_name: str, recipe_tokens: list[str]):
        try:
            update_result = self._collection.update_one(
                {"name": recipe_name},
                {"$addToSet": {"tags": {"$each": recipe_tokens}}}
            )
            return update_result
        except Exception as e:
            raise Exception(f"Failed to add tokens to recipe tags! - {str(e)}")


def add_tokens_by_id(self, recipe_id: str, recipe_tokens: list[str]):
    try:
        update_result = self._collection.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$addToSet": {"tags": {"$each": recipe_tokens}}}
        )
        return update_result
    except Exception as e:
        raise Exception(f"Failed to add tokens to recipe tags! - {str(e)}")


def get_recipe_ratings(self, parent_name: str, start: int, offset: int) -> List[dict]:
    try:
        recipe = self._collection.find_one({"name": parent_name})
        if not recipe:
            raise Exception("Recipe not found")
        ratings = recipe.get("ratings", [])
        return ratings[start:start + offset]
    except Exception as e:
        raise Exception(f"Failed to get recipe ratings: {str(e)}")


def get_rating_replies(self, parent_name: str, start: int, offset: int) -> List[dict]:
    try:
        recipe = self._collection.find_one({"name": parent_name})
        if not recipe:
            raise Exception("Recipe not found")
        ratings = recipe.get("ratings", [])
        # assume all ratings are replies
        return ratings[start:start + offset]
    except Exception as e:
        raise Exception(f"Failed to get rating replies: {str(e)}")


def add_rating(self, data: dict) -> ObjectId:
    try:
        recipe_name = data.get("parent_name")
        recipe = self._collection.find_one({"name": recipe_name})
        if not recipe:
            raise Exception("Recipe not found")
        rating = {
            "_id": ObjectId(),
            "updatedAt": datetime.utcnow(),
            "name": data.get("name"),
            "authorId": ObjectId(data.get("authorId")),
            "recipeId": recipe["_id"],
            "rating": data.get("rating"),
            "description": data.get("description")
        }
        # Update ratingSum and ratingCount
        new_rating_sum = recipe.get("ratingSum", 0) + rating["rating"]
        new_rating_count = recipe.get("ratingCount", 0) + 1
        self._collection.update_one(
            {"name": recipe_name},
            {"$push": {"ratings": rating}, "$set": {"ratingSum": new_rating_sum, "ratingCount": new_rating_count}}
        )
        return rating["_id"]
    except Exception as e:
        raise Exception(f"Failed to add rating: {str(e)}")


def edit_rating(self, parent_name: str, rating_id: str, new_rating: int, new_description: str):
    try:
        # Find the rating in the recipe
        rating_index = f"ratings.{rating_id}"
        self._collection.update_one(
            {"name": parent_name, rating_index: {"$exists": True}},
            {"$set": {f"{rating_index}.rating": new_rating, f"{rating_index}.description": new_description}}
        )
    except Exception as e:
        raise Exception(f"Failed to edit rating: {str(e)}")


def delete_rating(self, rating_id: str):
    try:
        # remove the rating from the recipe
        self._collection.update_one(
            {"ratings._id": ObjectId(rating_id)},
            {"$pull": {"ratings": {"_id": ObjectId(rating_id)}}}
        )
    except Exception as e:
        raise Exception(f"Failed to delete rating: {str(e)}")
