from pymongo import MongoClient

from constants import MONGO_URL


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URL)


class FollowCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.follow


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.user


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.recipe


class RatingCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.rating


class ReportCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.report


class ExpiringTokenCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.cooking_app.expiring_token
