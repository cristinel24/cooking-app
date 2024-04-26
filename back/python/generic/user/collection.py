import json
import os
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


def parse_json(data):
    return json.loads(json_util.dumps(data))


class RecipeCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.recipe

    def find_saved_recipe_by_id(self, recipe_id: str) -> dict:
        recipe = self._collection.find_one({"_id": recipe_id}, {"_id": 0})

        return recipe


class FollowCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.follow

    def find_follower_by_id(self, follower_id: str) -> dict:
        follower = self._collection.find_one({"_id": follower_id}, {"_id": 0})

        return follower


class UserCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.user

    def get_user_by_name(self, name: str) -> dict:
        user = self._collection.find_one({"name": name})
        return parse_json(user)

    def change_account_data(self, name: str, data: AccountChangeData) -> dict:
        update_operations = []

        if data.display_name:
            update_operations.append(UpdateOne({"name": name}, {"$set": {"displayName": data.display_name}}))
        if data.icon:
            update_operations.append(UpdateOne({"name": name}, {"$set": {"icon": data.icon}}))
        if data.description:
            update_operations.append(UpdateOne({"name": name}, {"$set": {"description": data.description}}))
        if data.allergens:
            update_operations.append(UpdateOne({"name": name}, {"$set": {"allergens": data.allergens}}))

        if update_operations:
            self._collection.bulk_write(update_operations)

        return {"name": name, "data": data.dict()}

    def save_recipe(self, name: str, recipe_name: str) -> dict:
        recipe = RecipeCollection()._collection.find_one({"name": recipe_name})
        recipe_id = recipe["_id"]
        self._collection.update_one(
            {"name": name},
            {"$push": {"savedRecipes": recipe_id}}
        )

        return {"name": name, "recipe": recipe_name}

    def unsave_recipe(self, name: str, recipe_name: str) -> dict:
        recipe = RecipeCollection()._collection.find_one({"name": recipe_name})
        recipe_id = recipe["_id"]
        self._collection.update_one(
            {"name": name},
            {"$pull": {"savedRecipes": recipe_id}}
        )

        return {"name": name, "recipe": recipe_name}

    def add_follow(self, name: str, follow_name: str) -> dict:
        user = self._collection.find_one({"name": name})
        follower = self._collection.find_one({"name": follow_name})

        if not user or not follower:
            return {"error": "One or both users not found"}

        name_id = user["_id"]
        follow_id = follower["_id"]

        dict_follow = {"userId": name_id, "followsId": follow_id}

        FollowCollection()._collection.insert_one(dict_follow)

        return {"userId": str(name_id), "followsId": str(follow_id)}

    def delete_follow(self, follower_name: str, followee_name: str) -> dict:
        user = self._collection.find_one({"name": followee_name})
        follower = self._collection.find_one({"name": follower_name})

        if not user or not follower:
            return {"error": "One or both users not found"}

        name_id = user["_id"]
        follow_id = follower["_id"]

        dict_follow = {"userId": name_id, "followsId": follow_id}

        FollowCollection()._collection.delete_one(dict_follow)

        return {"userId": str(name_id), "followsId": str(follow_id)}

    def get_following(self, name: str, start: int, count: int) -> dict:
        try:
            user = self._collection.find_one({"name": name})
            if not user:
                return {"error": "User not found"}
        except Exception as e:
            return {"error": f"Database error: {str(e)}"}

        user_id = user["_id"]

        following_cursor = FollowCollection()._collection.find({"userId": user_id}, {"_id": 0, "followsId": 1}).skip(start).limit(count)

        following_list = list(following_cursor)
        if not following_list:
            return {"error": "No following users found"}

        for i in range(len(following_list)):
            follows_id = following_list[i]["followsId"]
            followed_user_details = self._collection.find_one({"_id": follows_id}, {"displayName": 1, "_id": 0})
            if followed_user_details:
                following_list[i] = followed_user_details
            else:
                following_list[i] = {"error": "Followed user details not found"}

        follow_dict = {"following": following_list}

        return follow_dict

    def get_recipes(self, name: str) -> dict:
        try:
            user = self._collection.find_one({"name": name}, {"_id": 0})
        except Exception as e:
            raise Exception(f"User not found! - {str(e)}")

        saved_recipes_list = user["savedRecipes"]

        for i in range(len(saved_recipes_list)):
            saved_recipe_id = saved_recipes_list[i]
            saved_recipes_list[i] = RecipeCollection().find_saved_recipe_by_id(saved_recipe_id)

        user_dict = {
            "name": user["name"],
            "savedRecipes": saved_recipes_list
        }

        user_json = parse_json(user_dict)

        return user_json

    def find_follower_by_id(self, following_id):
        user = self._collection.find_one({"_id": following_id}, {"_id": 0}, {"name": 1}, {"displayName": 1})
        return parse_json(user)
