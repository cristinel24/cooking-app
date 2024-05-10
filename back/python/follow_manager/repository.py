from pymongo import MongoClient, errors

from constants import MONGO_URL, FOLLOWERS_PROJECTION, FOLLOWING_PROJECTION


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.follow

    def get_followers(self, user_id: str) -> list[str]:
        try:
            return list(map(lambda follower: follower["userId"],
                            self._collection.find({"followsId": user_id}, FOLLOWERS_PROJECTION)))
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get followers! - {str(e)}")

    def get_following(self, user_id: str) -> list[str]:
        try:
            return list(map(lambda following: following["followsId"],
                            self._collection.find({"userId": user_id}, FOLLOWING_PROJECTION)))
        except errors.PyMongoError as e:
            raise Exception(f"Failed to get followers! - {str(e)}")

    def add_follow(self, user_id: str, follows_id: str):
        pass

    def delete_follow(self, user_id: str, follows_id: str):
        pass
