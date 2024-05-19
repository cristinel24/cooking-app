from fastapi import status
from pymongo import MongoClient, timeout, errors
from pymongo.client_session import ClientSession

from constants import MONGO_URI, ErrorCodes, DB_NAME, MAX_TIMEOUT_TIME_SECONDS
from exception import RecipeCreatorException
from utils import match_collection_error


class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is None:
            self._connection = MongoClient(MONGO_URI)
        else:
            self._connection = connection
        try:
            self._connection.admin.command("ping")
        except ConnectionError:
            raise RecipeCreatorException(
                ErrorCodes.DB_CONNECTION_FAILURE.value,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_connection(self) -> MongoClient:
        return self._connection


class UserCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def update_user(self, user_id: str, recipe_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.update_one(
                    {"id": user_id},
                    {"$push": {"recipes": recipe_id}},
                    session=session
                )
        except errors.PyMongoError as e:
            raise match_collection_error(e)


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def insert_recipe(self, recipe: dict, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                self._collection.insert_one(recipe, session=session)
        except errors.PyMongoError as e:
            raise match_collection_error(e)
