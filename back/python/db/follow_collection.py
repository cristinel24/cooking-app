import pymongo

from bson import ObjectId
from pymongo import MongoClient
from pymongo import errors

from db.mongo_collection import MongoCollection


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._db = self._connection.cooking_app
        self._collection = self._db.follow

    def insert_follow(self, user_id: ObjectId, follows_id: ObjectId) -> ObjectId:
        try:
            return self._collection.insert_one({
                "userId": user_id,
                "followsId": follows_id
            }).inserted_id
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to insert follow relationship! - {str(e)}")

    def get_following_by_user_id(self, user_id: ObjectId, start: int, count: int) -> list:
        try:
            followings = list(
                self._collection
                .find({"userId": user_id}, {"_id": 0, "followsId": 1})
                .skip(start)
                .limit(count)
            )
            followings = map(lambda item: item["followsId"], followings)
            return list(followings)
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get user following! - {str(e)}")

    def get_followers_by_user_id(self, user_id: ObjectId, start: int, count: int) -> list:
        try:
            followers = list(
                self._collection
                .find({"followsId": user_id}, {"_id": 0, "userId": 1})
                .skip(start)
                .limit(count)
            )
            followers = map(lambda item: item["userId"], followers)
            return list(followers)
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get user followers! - {str(e)}")

    def get_follow(self, user_id: ObjectId, follows_id: ObjectId) -> dict:
        try:
            return self._collection.find_one({
                "userId": user_id,
                "followsId": follows_id
            })
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to get follow relationship! - {str(e)}")

    def delete_follow(self, user_id: ObjectId, follows_id: ObjectId) -> None:
        try:
            self._collection.delete_one({
                "userId": user_id,
                "followsId": follows_id
            })
        except pymongo.errors.PyMongoError as e:
            raise Exception(f"Failed to delete follow relationship! - {str(e)}")
