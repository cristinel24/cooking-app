import json
import os
from pprint import pprint

from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util

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

    def get_user_by_name(self, name: str) -> dict:
        user = self._collection.find_one({"name": name})

        user_json = parse_json(user)
        return user_json
