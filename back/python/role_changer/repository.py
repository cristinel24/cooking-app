import os
from pymongo import MongoClient, errors, timeout
from bson import ObjectId
from constants import *

class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true"))
        self._collection = self._connection['cooking_app']['user']

    def update_roles(self, user_id: str, roles: int) -> None:
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                if roles < UserRoles.ACTIVE or roles >= UserRoles.BANNED*2:
                   return ErrorCodes.NONEXISTENT_ROLES
                
                if roles & UserRoles.BANNED:
                    result = self._collection.update_one(
                        {"id": user_id},
                        {"$bit": {"roles": {"or": roles}}}
                        )
                
                else:
                    result = self._collection.update_one(
                        {"id": user_id},
                        {"$set": {"roles": roles}}
                        )

                if result.matched_count==0:
                    return ErrorCodes.NONEXISTENT_USER
                return 0
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_ROLES
           