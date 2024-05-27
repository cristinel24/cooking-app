import pymongo
from pymongo import MongoClient
from fastapi import status
from exceptions import LoginException
from constants import *


class MongoCollection:
    def __init__(self):
        self._connection = MongoClient(MONGO_URI)


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.get_database(DB_NAME).user

    def find_user_by_name(self, name: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_SECONDS):
                user = self._collection.find_one({"username": name}, USER_PROJECTION)
                if not user:
                    raise LoginException(Errors.INVALID_CREDS, status.HTTP_401_UNAUTHORIZED)
                return user
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise LoginException(Errors.DB_TIMEOUT, status.HTTP_504_GATEWAY_TIMEOUT)
            raise LoginException(Errors.DB_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def find_user_by_mail(self, mail: str):
        try:
            with pymongo.timeout(MAX_TIMEOUT_SECONDS):
                user = self._collection.find_one({"email": mail}, USER_PROJECTION)
                if not user:
                    raise LoginException(Errors.INVALID_CREDS, status.HTTP_401_UNAUTHORIZED)
                return user
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise LoginException(Errors.DB_TIMEOUT, status.HTTP_504_GATEWAY_TIMEOUT)
            raise LoginException(Errors.DB_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)
