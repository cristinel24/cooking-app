from fastapi import status
from pymongo import MongoClient, errors, timeout

from constants import DB_NAME, MAX_TIMEOUT_TIME_SECONDS, MONGO_URI, ErrorCodes
from exception import FollowManagerException
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is None:
            self._connection = MongoClient(MONGO_URI)
        else:
            self._connection = connection
        try:
            self._connection.admin.command("ping")
        except ConnectionError:
            raise FollowManagerException(
                ErrorCodes.DB_CONNECTION_FAILURE.value,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def ping_user(self, user_id: str) -> bool:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                if self._collection.find_one({"id": user_id}, {"_id": 0, "id": 1}) is not None:
                    return True
        except errors.PyMongoError as e:
            raise match_collection_error(e)
        return False


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).follow

    def get_followers_count(self, user_id: str) -> int:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return self._collection.count_documents({"followsId": user_id})
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def get_followers(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return list(
                    map(
                        lambda following: following["userId"],
                        self._collection
                        .find({"followsId": user_id})
                        .sort({"_id": -1})
                        .skip(start)
                        .limit(count)
                    )
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def get_following_count(self, user_id: str) -> int:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return self._collection.count_documents({"userId": user_id})
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def get_following(self, user_id: str, start: int, count: int) -> list[str]:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return list(
                    map(
                        lambda following: following["followsId"],
                        self._collection
                        .find({"userId": user_id})
                        .sort({"_id": -1})
                        .skip(start)
                        .limit(count)
                    )
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def get_follow(self, user_id: str, follows_id: str):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return self._collection.find_one({
                    "userId": user_id,
                    "followsId": follows_id
                })
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def add_follow(self, user_id: str, follows_id: str):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.insert_one({
                    "userId": user_id,
                    "followsId": follows_id
                })
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def delete_follow(self, user_id: str, follows_id: str):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.delete_one({
                    "userId": user_id,
                    "followsId": follows_id
                })
        except errors.PyMongoError as e:
            raise match_collection_error(e)
