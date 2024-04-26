import json
import os
from pprint import pprint

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from bson import json_util

from user.constants import DEFAULT_MONGO_URI
from user.schemas import AccountChangeData

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

    def find_recipe_by_id(self, recipe_id: str) -> dict:
        recipe = self._collection.find_one({"_id": recipe_id})

        return recipe


class FollowCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.follow


class UserCollection(MongoCollection):
    def __init__(self, client: MongoClient | None = None):
        super().__init__(client)
        self._db = self._client.cooking_app
        self._collection = self._db.user
        self.recipe_collection = RecipeCollection()

    def get_user_by_name(self, name: str) -> dict:
        try:
            user = self._collection.find_one({"name": name}, {"_id": 0})
        except Exception as e:
            raise Exception(f"User not found! - {str(e)}")

        recipes_list = user["recipes"]
        saved_recipes_list = user["savedRecipes"]

        for i in range(len(recipes_list)):
            recipe_id = recipes_list[i]
            recipes_list[i] = self.recipe_collection.find_recipe_by_id(recipe_id)
            del recipes_list[i]["_id"]

        for i in range(len(saved_recipes_list)):
            saved_recipe_id = saved_recipes_list[i]
            saved_recipes_list[i] = self.recipe_collection.find_recipe_by_id(saved_recipe_id)
            del saved_recipes_list[i]["_id"]

        user_dict = {
            "name": user["name"],
            "displayName": user["displayName"],
            "icon": user["icon"],
            "allergens": user["allergens"],
            "recipes": recipes_list,
            "savedRecipes": saved_recipes_list
        }

        user_json = parse_json(user_dict)

        return user_json

    def change_account_data(self, name: str, data: AccountChangeData) -> dict:
        update_operations = dict()

        if data.display_name:
            update_operations["displayName"] = data.display_name
        if data.icon:
            update_operations["icon"] = data.icon
        if data.description:
            update_operations["description"] = data.description
        if data.allergens:
            update_operations["allergens"] = data.allergens

        if update_operations:
            self._collection.update_one({"name": name}, {"$set": update_operations})

        return {"name": name, "data": data.dict()}

    def add_search(self, name: str, search: str) -> dict:
        self._collection.update_one({"name": name}, {"$push": {"searchHistory": search}})

        return {"name": name, "search": search}

    def get_search_history(self, name: str) -> dict:
        user = self._collection.find_one({"name": name})
        search_history = user["searchHistory"]

        return {"name": name, "searchHistory": search_history}

    def clear_search_history(self, name: str) -> dict:
        self._collection.update_one({"name": name}, {"$set": {"searchHistory": []}})

        return {"name": name, "searchHistory": []}

    def add_message(self, name: str, message: str) -> dict:
        self._collection.update_one({"name": name}, {"$push": {"messageHistory": message}})

        return {"name": name, "message": message}

    def get_message_history(self, name: str) -> dict:
        user = self._collection.find_one({"name": name})
        message_history = user["messageHistory"]

        return {"name": name, "messageHistory": message_history}

    def clear_message_history(self, name: str) -> dict:
        self._collection.update_one({"name": name}, {"$set": {"messageHistory": []}})

        return {"name": name, "messageHistory": []}
