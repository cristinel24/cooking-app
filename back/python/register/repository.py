import os
import pymongo
import exceptions
import constants
import schemas

from fastapi import status
from utils import match_collection_error
from pymongo import errors


class MongoCollection:
    def __init__(self):
        self._connection = pymongo.MongoClient(os.getenv("MONGO_URI",
                                                         "mongodb://localhost:27017/?directConnection=true"))


class UserCollection(MongoCollection):
    def __init__(self):
        super().__init__()
        self._collection = self._connection.cooking_app.user

    def find_user_by_name(self, name: str):
        with pymongo.timeout(constants.MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one(
                    {"username": name},
                    schemas.USER_PROJECTION
                )
                if user:
                    raise exceptions.RegisterException(
                        error_code=constants.ErrorCodes.USERNAME_ALREADY_EXISTS,
                        status_code=400
                    )
                return 1
            except errors.PyMongoError as e:
                raise match_collection_error(e)

    def find_user_by_email(self, email: str):
        with pymongo.timeout(constants.MAX_TIMEOUT_SECONDS):
            try:
                user = self._collection.find_one(
                    {"email": email},
                    schemas.USER_PROJECTION
                )
                if user:
                    raise exceptions.RegisterException(
                        error_code=constants.ErrorCodes.EMAIL_ALREADY_REGISTERED,
                        status_code=400
                    )
                return 1
            except errors.PyMongoError as e:
                raise match_collection_error(e)


