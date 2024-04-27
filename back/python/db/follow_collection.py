from bson import ObjectId
from pymongo import MongoClient

from db.mongo_collection import MongoCollection


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._db = self._connection.cooking_app
        self._collection = self._db.follow

    def insert_follow(self, user_id: ObjectId, follows_id: ObjectId) -> ObjectId:
        return self._collection.insert_one({
            "userId": user_id,
            "followsId": follows_id
        }).inserted_id

    def get_following_by_user_id(self, user_id: ObjectId, start: int, count: int) -> list:
        followings = list(
                        self._collection
                        .find({"userId": user_id}, {"_id": 0, "followsId": 1})
                        .skip(start)
                        .limit(count)
                        )
        followings = map(lambda item: item["followsId"], followings)
        return list(followings)

    def get_followers_by_user_id(self, user_id: ObjectId, start: int, count: int) -> list:
        followers = list(self._collection
                         .find({"followsId": user_id}, {"_id": 0, "userId": 1})
                         .skip(start)
                         .limit(count)
                         )
        followers = map(lambda item: item["userId"], followers)
        return list(followers)

    def get_follow(self, user_id: ObjectId, follows_id: ObjectId) -> dict:
        return self._collection.find_one({
            "userId": user_id,
            "followsId": follows_id
        })

    def delete_follow(self, user_id: ObjectId, follows_id: ObjectId) -> None:
        self._collection.delete_one({
            "userId": user_id,
            "followsId": follows_id
        })
