import os
from pymongo import MongoClient, errors, timeout
from bson import ObjectId
from constants import *

class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))

    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection['cooking_app']['user']

    def update_roles(self, user_id: str, roles: int) -> None:
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                item = self._collection.find_one({"_id": ObjectId(user_id)})
            
                if item is None:
                   return ErrorCodes.NONEXISTENT_USER

                elif roles < UserRoles.ACTIVE or roles > UserRoles.BANNED:
                   return ErrorCodes.NONEXISTENT_ROLES
                else:
                    self._collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"roles": roles}}
                    )
                return 0
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_ROLES