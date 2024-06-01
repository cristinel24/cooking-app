import pymongo
from bson import ObjectId
from fastapi import status
from pymongo import errors

import exceptions
from constants import DB_NAME, MAX_TIMEOUT_TIME_SECONDS, MONGO_URI, ErrorCodes


class MongoCollection:
    def __init__(self, connection: pymongo.MongoClient | None = None):
        self._connection = connection if connection is not None else pymongo.MongoClient(MONGO_URI)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe

    def get_recipe_by_id(self, recipe_id: str, projection_arg: dict, is_viewed: bool) -> dict:
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                item = self._collection.find_one({"id": recipe_id}, projection=projection_arg)
                if item is None:
                    raise exceptions.RecipeException(status.HTTP_404_NOT_FOUND, ErrorCodes.NONEXISTENT_RECIPE)

                recipe__id = ObjectId(item["_id"])
                item["createdAt"] = recipe__id.generation_time
                item.pop("_id")
                if is_viewed:
                    self._collection.update_one({"id": recipe_id}, {"$inc": {"viewCount": 1}})
                return item
        except errors.PyMongoError:
            raise exceptions.RecipeException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.SERVER_ERROR)

    def get_recipes(self, recipe_ids: list[str], projection: dict):
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                result = self._collection.find({"id": {"$in": recipe_ids}}, projection)
                recipe_cards = list()
                for recipe_card in result:
                    recipe__id = ObjectId(recipe_card["_id"])
                    recipe_card["createdAt"] = recipe__id.generation_time
                    recipe_card.pop("_id")
                    recipe_cards.append(recipe_card)
                return recipe_cards
        except errors.PyMongoError as e:
            raise exceptions.RecipeException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.SERVER_ERROR)


class UserCollection(MongoCollection):
    def __init__(self, connection: pymongo.MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def is_favorite_recipe(self, user_id: str, recipe_id: str) -> bool:
        try:
            with pymongo.timeout(MAX_TIMEOUT_TIME_SECONDS):
                item = self._collection.find_one({"id": user_id, "savedRecipes": recipe_id})
                return item is not None
        except errors.PyMongoError as e:
            raise exceptions.RecipeException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.SERVER_ERROR)
