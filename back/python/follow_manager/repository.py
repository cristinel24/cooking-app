from pymongo import MongoClient, errors

from constants import MONGO_URL


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.follow

    def get_followers(self, user_id: str) -> list[str]:
        try:
            return list(
                map(
                    lambda following: following["userId"],
                    self._collection
                    .find({"followsId": user_id})
                    .sort({"_id": -1})
                )
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get followers! - {str(e)}")

    def get_following(self, user_id: str) -> list[str]:
        try:
            return list(
                map(
                    lambda following: following["followsId"],
                    self._collection
                    .find({"userId": user_id})
                    .sort({"_id": -1})
                )
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get following! - {str(e)}")

    def add_follow(self, user_id: str, follows_id: str):
        try:
            self._collection.insert_one({
                "userId": user_id,
                "followsId": follows_id
            })
        except errors.PyMongoError as e:
            raise Exception(f"Failed to insert follow relationship! - {str(e)}")

    def delete_follow(self, user_id: str, follows_id: str):
        try:
            self._collection.delete_one({
                "userId": user_id,
                "followsId": follows_id
            })
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete follow relationship! - {str(e)}")
