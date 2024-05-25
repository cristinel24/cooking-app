from constants import *
from exceptions import RoleChangerException
from fastapi import status
from pymongo import MongoClient, errors, timeout
from schemas import *


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is None:
            self._connection = MongoClient(MONGO_URI)
        else:
            self._connection = connection
        try:
            self._connection.admin.command("ping")
        except ConnectionError:
            raise RoleChangerException(
                ErrorCodes.DB_CONNECTION_FAILURE.value,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user


    def get_user_roles(self, user_id: str) -> int:
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                user = self._collection.find_one({"id": user_id})
                if not user:
                    raise RoleChangerException(status_code=status.HTTP_404_NOT_FOUND, error_code=ErrorCodes.NONEXISTENT_USER.value)

                return int(user.get("roles", UserRoles.ACTIVE))
        except errors.PyMongoError as e:
            if e.timeout:
                raise RoleChangerException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, error_code=ErrorCodes.DB_TIMEOUT.value)
            raise RoleChangerException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code=ErrorCodes.DB_ERROR.value)


    def update_roles(self, user_id: str, roles: int):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.update_one({"id": user_id}, {"$set": { "roles": roles}})
        except errors.PyMongoError as e:
            if e.timeout:
                raise RoleChangerException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, error_code=ErrorCodes.DB_TIMEOUT.value)
            raise RoleChangerException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code=ErrorCodes.DB_ERROR.value)
