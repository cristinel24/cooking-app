from pymongo import MongoClient, errors, timeout
from fastapi import status

from constants import MONGO_URL, ErrorCodes, MAX_TIMEOUT_TIME_SECONDS
from exception import FollowManagerException
from utils import match_collection_error


class MongoCollection:
    _connection = None

    def __init__(self, connection: MongoClient | None = None):
        if self._connection is None:
            self._connection = MongoClient(MONGO_URL)
            try:
                self._connection.admin.command('ping')
            except ConnectionError:
                raise FollowManagerException(ErrorCodes.DB_CONNECTION_FAILURE, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            self._connection = connection


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.follow

    def get_followers(self, user_id: str) -> list[str]:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return list(
                    map(
                        lambda following: following["userId"],
                        self._collection
                        .find({"followsId": user_id})
                        .sort({"_id": -1})
                    )
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    def get_following(self, user_id: str) -> list[str]:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                return list(
                    map(
                        lambda following: following["followsId"],
                        self._collection
                        .find({"userId": user_id})
                        .sort({"_id": -1})
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
