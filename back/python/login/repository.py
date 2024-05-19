import pymongo
from pymongo import MongoClient, errors
from exceptions import LoginException
from constants import MAX_TIMEOUT_SECONDS, Errors, MONGO_URI, DB_NAME
from schemas import USER_PROJECTION


class MongoCollection:
    def __init__(self):
        self._connection = MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).user

    def find_user_by_name(self, name: str):
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one({"username": name}, USER_PROJECTION)
                if not user:
                    raise LoginException(Errors.INVALID_CREDS, "invalid credentials")
                return user
            except pymongo.errors.PyMongoError:
                raise LoginException(Errors.DB_ERROR, "server error")

    def find_user_by_mail(self, mail: str):
        with pymongo.timeout(MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one({"email": mail})
                if not user:
                    raise LoginException(Errors.INVALID_CREDS, "invalid credentials")
                return user
            except pymongo.errors.PyMongoError:
                raise LoginException(Errors.DB_ERROR, "server error")
