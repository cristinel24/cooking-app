import os

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

from user.constants import DEFAULT_MONGO_URI

load_dotenv()

"""
    TODO: EXCEPTION HANDLING
"""


class MongoCollection:
    def __init__(self, client: MongoClient | None = None):
        super().__init__()
        self._client = client \
            if client is not None else MongoClient(os.getenv("MONGO_URI", DEFAULT_MONGO_URI))


class RecipeCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.recipe

    def find_recipe_by_id(self, recipe_id: str) -> dict:
        recipe = self._collection.find_one({"_id": ObjectId(recipe_id)})
        return recipe

    def find_recipe_by_name(self, recipe_name: str) -> dict:
        return self._collection.find_one({"name": recipe_name})

    def find_recipe_id_by_name(self, recipe_name: str) -> ObjectId:
        return self._collection.find_one(
            {"name": recipe_name},
            {"_id": 1}
        )["_id"]


class FollowCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.follow

    def insert_follow(self, user_id: ObjectId, follows_id: ObjectId) -> None:
        self._collection.insert_one({
            "userId": user_id,
            "followsId": follows_id
        })

    def get_following_by_user_id(self, user_id: ObjectId, start: int, count: int) -> list:
        followings = list(self._collection
                          .find({"userId": user_id}, {"_id": 0, "followsId": 1})
                          .skip(start)
                          .limit(count)
                          )
        followings = map(lambda item: item["followsId"], followings)
        return list(followings)

    def get_followers_by_user_id(self, user_id: ObjectId, start: int, count: int) -> list:
        followers = list(self._collection
                         .find({"followsId": user_id}, {"_id": 0, "userId": 1})
                         .skip(start)
                         .limit(count)
                         )
        followers = map(lambda item: item["userId"], followers)
        return list(followers)

    def get_follow(self, user_id: ObjectId, follows_id: ObjectId) -> dict:
        return self._collection.find_one({
            "userId": user_id,
            "followsId": follows_id
        })

    def delete_follow(self, user_id: ObjectId, follows_id: ObjectId) -> None:
        self._collection.delete_one({
            "userId": user_id,
            "followsId": follows_id
        })


class UserCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.user

    def get_user_id_by_name(self, user_name: str) -> ObjectId:
        return self._collection.find_one(
            {"name": user_name},
            {"_id": 1}
        )["_id"]

    def get_user_name_by_id(self, user_id: ObjectId) -> str:
        return self._collection.find_one(
            {"_id": user_id},
            {
                "name": 1,
                "_id": 0
            }
        )["name"]

    def get_user_by_name(self, user_name: str) -> dict:
        user = self._collection.find_one({"name": user_name})
        return user

    def update_user_by_name(self, user_name: str, updated_fields: dict) -> None:
        for updated_field in updated_fields.items():
            self._collection.update_one(
                {"name": user_name},
                {"$set": {updated_field[0]: updated_field[1]}}
            )

    def update_saved_recipes_by_name(self, user_name: str, recipe_id: str) -> None:
        self._collection.update_one(
            {"name": user_name},
            {"$push": {"savedRecipes": recipe_id}}
        )

    def delete_saved_recipe_by_name(self, user_name: str, recipe_id: ObjectId) -> None:
        self._collection.update_one(
            {"name": user_name},
            {"$pull": {"savedRecipes": recipe_id}}
        )
