import pymongo
from fastapi import status
from pymongo import MongoClient, errors

from constants import DB_NAME, MONGO_URI, DB_TIMEOUT, ErrorCodes
from exceptions import AIException


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class DBWrapper:

    def __init__(self):
        self._connection = MongoClient(MONGO_URI)
        try:
            with pymongo.timeout(15):
                self._admin_database.command("ping")
        except Exception:
            raise AIException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                error_code=ErrorCodes.DB_CONNECTION_FAILURE
            )

    @property
    def _admin_database(self):
        return self._connection.admin

    @property
    def _recipe_collection(self):
        return self._connection.get_database(DB_NAME).recipe

    @property
    def _user_collection(self):
        return self._connection.get_database(DB_NAME).user

    @staticmethod
    def __get_from_collection(collection, entry_id: str):
        try:
            with pymongo.timeout(DB_TIMEOUT):
                item = collection.find_one({"id": entry_id})
                return item
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise AIException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    error_code=ErrorCodes.DB_CONNECTION_TIMEOUT
                )
            raise AIException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.DB_CONNECTION_NON_TIMEOUT
            )

    def get_recipe(self, recipe_id: str) -> dict:
        return self.__get_from_collection(self._recipe_collection, recipe_id)

    def get_user_context(self, user_id: str) -> dict:
        return self.__get_from_collection(self._user_collection, user_id)

    def append_to_user_message_history(self, user_id: str, new_message: str):
        try:
            with pymongo.timeout(DB_TIMEOUT):
                pass
        except AIException as e:
            raise e
        except pymongo.errors.PyMongoError as e:
            if e.timeout:
                raise AIException(
                    status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                    error_code=ErrorCodes.DB_CONNECTION_TIMEOUT
                )
            raise AIException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=ErrorCodes.DB_CONNECTION_NON_TIMEOUT
            )
