import pymongo
from pymongo import MongoClient, errors
from pymongo.client_session import ClientSession
from constants import MONGO_URI, DB_NAME, ErrorCodes, MONGO_TIMEOUT
from exception import ProfileDataChangerException
from fastapi import status
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: MongoClient = None):
        self.connection = connection if connection is not None else MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient = None):
        super().__init__(connection)
        db = self.connection.get_database(DB_NAME)
        self._collection = db.user

    def patch_user(self, user_id: str, changes: dict, allergens_to_add: list[str], allergens_to_remove: list[str],
                   session: ClientSession) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                update_pipeline = [
                    {"$set": changes},
                    {"$set": {
                        "allergens": {
                            "$setUnion": [
                                {"$setDifference": ["$allergens", allergens_to_remove]},
                                allergens_to_add
                            ]
                        }
                    }}
                ]
                updated = self._collection.update_one({"id": user_id}, update_pipeline, session=session)
                if updated.matched_count == 0:
                    raise ProfileDataChangerException(status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND.value)
        except errors.PyMongoError as e:
            match_collection_error(e)

    def get_user_allergens(self, user_id: str) -> set[str]:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                allergens = self._collection.find_one({"id": user_id}, projection={"_id": 0, "allergens": 1})
                if not allergens:
                    raise ProfileDataChangerException(status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND.value)
                return set(allergens["allergens"])
        except errors.PyMongoError as e:
            match_collection_error(e)
