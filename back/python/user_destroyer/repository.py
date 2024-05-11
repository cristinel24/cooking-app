from pymongo import MongoClient, errors

from constants import MONGO_URL


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.follow

    def delete_follows_by_user_id(self, user_id: str):
        try:
            self._collection.delete_many({"userId": user_id})
            self._collection.delete_many({"followsId": user_id})
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete follow relationships! - {str(e)}")


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user

    def delete_user_by_user_id(self, user_id: str):
        try:
            self._collection.delete_one({"id": user_id})
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete user! - {str(e)}")


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe

    def update_author_id_by_user_id(self, user_id: str, new_user_id: str):
        try:
            self._collection.update_many(
                {"authorId": user_id},
                {"$set": {"authorId": new_user_id}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update recipes for deleted user! - {str(e)}")


class RatingCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.rating

    def update_author_id_by_user_id(self, user_id: str, new_user_id: str):
        try:
            self._collection.update_many(
                {"authorId": user_id},
                {"$set": {"authorId": new_user_id}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update ratings for deleted user! - {str(e)}")


class ReportCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.report

    def update_author_id_by_user_id(self, user_id: str, new_user_id: str):
        try:
            self._collection.update_many(
                {"authorId": user_id},
                {"$set": {"authorId": new_user_id}}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to update deleted user authorId! - {str(e)}")

    def delete_reported_id_by_user_id(self, user_id: str):
        try:
            self._collection.delete_many(
                {"reportedId": user_id}
            )
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete reportedId! - {str(e)}")


class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.expiring_token

    def delete_expiring_tokens_by_user_id(self, user_id: str):
        try:
            self._collection.delete_many({"userId": user_id})
        except errors.PyMongoError as e:
            raise Exception(f"Failed to delete expiring tokens! - {str(e)}")
