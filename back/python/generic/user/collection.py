import json
import os
from pprint import pprint

from user.schemas import AccountChangeData
from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from bson import ObjectId, json_util

from user.constants import DEFAULT_MONGO_URI

load_dotenv()


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


recipe_collection = RecipeCollection()


class FollowCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.follow


follow_collection = FollowCollection()


class UserCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.user

    def get_user_by_name(self, user_name: str) -> dict:
        user = self._collection.find_one({"name": user_name})
        return user

    def update_user_by_name(self, user_name: str, updated_fields: dict):
        # todo Exception Handling
        for updated_field in updated_fields.items():
            self._collection.update_one(
                {"name": user_name},
                {"$set": {updated_field[0]: updated_field[1]}}
            )

    def update_saved_recipes_by_name(self, user_name: str, recipe_id: str) -> None:
        # todo Exception Handling
        self._collection.update_one(
            {"name": user_name},
            {"$push": {"savedRecipes": recipe_id}}
        )

    def unsave_recipe(self, user_name: str, recipe_name: str) -> dict:
        recipe = recipe_collection._collection.find_one({"name": recipe_name})
        recipe_id = recipe["_id"]
        self._collection.update_one(
            {"name": user_name},
            {"$pull": {"savedRecipes": recipe_id}}
        )

        return {"name": user_name, "recipe": recipe_name}

    def add_follow(self, user_name: str, follow_name: str) -> dict:
        user = self._collection.find_one({"name": user_name})
        follower = self._collection.find_one({"name": follow_name})

        if not user or not follower:
            return {"error": "One or both users not found"}

        name_id = user["_id"]
        follow_id = follower["_id"]

        dict_follow = {"userId": name_id, "followsId": follow_id}

        follow_collection._collection.insert_one(dict_follow)

        return {"follower": user_name, "followed": follow_name}

    def delete_follow(self, follower_name: str, followee_name: str) -> dict:
        user = self._collection.find_one({"name": followee_name})
        follower = self._collection.find_one({"name": follower_name})

        if not user or not follower:
            return {"error": "One or both users not found"}

        name_id = user["_id"]
        follow_id = follower["_id"]

        dict_follow = {"userId": name_id, "followsId": follow_id}

        follow_collection._collection.delete_one(dict_follow)

        return {"follower": follower_name, "followed": followee_name}

    def get_following(self, user_name: str, start: int, count: int) -> dict:
        try:
            user = self._collection.find_one({"name": user_name})
            if not user:
                return {"error": "User not found"}
        except Exception as e:
            return {"error": f"Database error: {str(e)}"}

        user_id = user["_id"]

        following_cursor = follow_collection._collection.find({"userId": user_id}, {"_id": 0, "followsId": 1}).skip(
            start).limit(count)

        following_list = list(following_cursor)
        if not following_list:
            return {"error": "No following users found"}

        for i in range(len(following_list)):
            follows_id = following_list[i]["followsId"]
            followed_user_details = self._collection.find_one({"_id": follows_id},
                                                              {"displayName": 1, "name": 1, "_id": 0})
            if followed_user_details:
                following_list[i] = followed_user_details
            else:
                following_list[i] = {"error": "Followed user details not found"}

        follow_dict = {"following": following_list}

        return follow_dict

    def get_followers(self, user_name: str, start: int, count: int) -> dict:
        try:
            user = self._collection.find_one({"name": user_name})
            if not user:
                return {"error": "User not found"}
        except Exception as e:
            return {"error": f"Database error: {str(e)}"}

        user_id = user["_id"]

        followers_cursor = follow_collection._collection.find({"followsId": user_id}, {"_id": 0, "userId": 1}).skip(
            start).limit(count)

        followers_list = list(followers_cursor)
        if not followers_list:
            return {"error": "No followers found"}

        for i in range(len(followers_list)):
            follower_id = followers_list[i]["userId"]
            follower_details = self._collection.find_one({"_id": follower_id}, {"displayName": 1, "name": 1, "_id": 0})
            if follower_details:
                followers_list[i] = follower_details
            else:
                followers_list[i] = {"error": "Follower details not found"}

        follow_dict = {"followers": followers_list}
        followers_json = parse_json(follow_dict)
        return followers_json
