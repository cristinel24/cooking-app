from fastapi import status
from pymongo import MongoClient, timeout, errors
from pymongo.client_session import ClientSession

from constants import MONGO_URI, ErrorCodes, DB_NAME, MAX_TIMEOUT_TIME_SECONDS
from exception import RecipeEditorException
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
            raise RecipeEditorException(
                ErrorCodes.DB_CONNECTION_FAILURE.value,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_connection(self) -> MongoClient:
        return self._connection


class RecipeCollection(MongoCollection):
    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe

    async def get_recipe_by_id(self, recipe_id: str, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                item = self._collection.find_one({"id": recipe_id}, session=session)
                if item is None:
                    raise RecipeEditorException(ErrorCodes.NONEXISTENT_RECIPE.value, status.HTTP_404_NOT_FOUND)
                return item
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    async def edit_recipe(self, recipe_id: str, recipe: dict, session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                update_dict = {"$set": recipe}
                self._collection.update_one({"id": recipe_id}, update_dict, session=session)
        except errors.PyMongoError as e:
            raise match_collection_error(e)

    async def restore_tokens(self, recipe_id: str, tokens: list[str], session: ClientSession):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                item = self._collection.find_one({"id": recipe_id}, session=session)
                if item is None:
                    raise RecipeEditorException(ErrorCodes.NONEXISTENT_RECIPE.value, status.HTTP_404_NOT_FOUND)
                self._collection.update_one({"id": recipe_id}, {"$set": {tokens}}, session=session)
        except errors.PyMongoError as e:
            raise match_collection_error(e)
