import os
import sys

##to import paths with vscode (pycharm makes this automatly)
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pymongo.errors
from pymongo import DeleteOne, MongoClient
from db import user_collection

from generic.recipe.schemas import RecipeData
from db.mongo_collection import MongoCollection
from bson import ObjectId
from datetime import datetime


class RecipeCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def get_recipe_by_name(self, recipe_name: str) -> dict:
        try:
            item = self._collection.find_one({"name": recipe_name})

            if item is None:
                # TODO: err code
                return {"ok": 1, "error": f"Recipe '{recipe_name}' is nonexistent"}

            recipe_data = {
                "ok": 0,
                "title": item["title"],
                "description": item["description"],
                "prepTime": item["prepTime"],
                "steps": item["steps"],
                "ingredients": item["ingredients"],
                "allergens": item["allergens"],
                "tags": item["tags"],
                "no_ratings": item["ratingCount"]
            }
            # TODO: exception handling
        except Exception as e:
            # TODO: err code
            return {"ok": 1, "error": f"Failed to get recipe by name: {e}"}
        return recipe_data

    def get_recipe_card(self, recipe_name: str) -> dict:
        try:
            item = self._collection.find_one({"name": recipe_name})

            if item is None:
                # TODO: err code
                return {"ok": 1, "error": f"Recipe '{recipe_name}' is nonexistent"}

            user = user_collection.UserCollection()

            recipe_data = {
                "ok": 0,
                # TODO: get_user() instead of get_user_by_id()
                "author": user.get_user_by_id(str(item["authorId"]))["username"],
                "title": item["title"],
                "description": item["description"],
                "prepTime": item["prepTime"],
                "allergens": item["allergens"],
                "tags": item["tags"],
            }
            # TODO: exception handling
        except Exception as e:
            # TODO: err code
            return {"ok": 1, "error": f"Failed to get recipe by name: {e}"}
        return recipe_data

    def insert_recipe(self, params) -> None:
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
                    "ratings": []
                }
            )
        # TODO: exception handling
        except Exception as e:
            print(e)
            # TODO: err code
            # return {"ok": 1, "error": f"Failed to insert recipe! - {str(e)}"}

    def delete_recipe_by_name(self, recipe_name: str) -> None:
        try:
            self._collection.delete_one({"name": recipe_name})
        # TODO: exception handling
        except Exception as e:
            print(e)

    def update_recipe_by_name(self, data: dict) -> None:
        try:
            item = self._collection.find_one({"name": data["name"]})

            if item is None:
                return
                # TODO: err code
                # return {"ok": 1, "error": f"Recipe '{recipe_name}' is nonexistent"}
            data["updatedAt"] = datetime.utcnow()
            data = {key: value for key, value in data.items() if value is not None}
            self._collection.update_one({"name": data["name"]}, {"$set": data})

            # TODO: exception handling
        except Exception as e:
            print(e)

    def add_tokens_by_name(self, recipe_name: str, recipe_tokens: list[str]) -> None:
        try:
            update_result = self._collection.update_one(
                {"name": recipe_name},
                {"$addToSet": {"tags": {"$each": recipe_tokens}}}
            )

        except Exception as e:
            print(e)
