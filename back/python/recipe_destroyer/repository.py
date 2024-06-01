from fastapi import status
from pymongo import MongoClient, errors, timeout
from pymongo.client_session import ClientSession

from constants import MAX_TIMEOUT_TIME_SECONDS, ErrorCodes, DB_NAME, MONGO_URI
from exception import RecipeDestroyerException
from utils import match_collection_error


class MongoCollection:

    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(MONGO_URI)

    def get_connection(self) -> MongoClient:
        return self._connection


class RecipeCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).recipe

    def delete_recipe(self, recipe_id: str, session: ClientSession | None = None):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                result = self._collection.delete_one({"id": recipe_id}, session=session)
                if result.deleted_count == 0:
                    raise RecipeDestroyerException(
                        error_code=ErrorCodes.RECIPE_NOT_FOUND,
                        status_code=status.HTTP_404_NOT_FOUND
                    )
        except RecipeDestroyerException as e:
            raise e
        except errors.PyMongoError as e:
            raise match_collection_error(e)


class UserCollection(MongoCollection):

    def __init__(self, connection: MongoClient | None = None):
        super().__init__(connection)
        self._collection = self._connection.get_database(DB_NAME).user

    def delete_recipe_from_users(self, recipe_id: str, user_id: str, session: ClientSession | None = None):
        try:
            with timeout(MAX_TIMEOUT_TIME_SECONDS):
                result = self._collection.update_many(
                    {"id": user_id},
                    {"$pull": {"recipes": recipe_id}},
                    session=session
                )
                if result.modified_count == 0:
                    raise RecipeDestroyerException(
                        error_code=ErrorCodes.RECIPE_NOT_FOUND_IN_USERS,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
        except RecipeDestroyerException as e:
            raise e
        except errors.PyMongoError as e:
            raise match_collection_error(e)
