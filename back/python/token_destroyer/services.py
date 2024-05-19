from repository import *
from constants import ErrorCodes
from exception import TokenDestroyerException
from fastapi import status
from pymongo import errors


client = MongoCollection()
expiring_token_collection = ExpiringTokenCollection(client.get_connection())


async def delete_token(token: str):
    with client.get_connection().start_session() as session:
        try:
            with session.start_transaction():
                token_data = expiring_token_collection.find_and_remove_token(token, session)
                if not token_data:
                    raise TokenDestroyerException(status.HTTP_404_NOT_FOUND, ErrorCodes.TOKEN_NOT_FOUND.value)
        except errors.PyMongoError:
            raise TokenDestroyerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.FAILED_TO_DELETE_TOKEN.value)

async def delete_user_tokens(user_id: str):
    with client.get_connection().start_session() as session:
        try:
            with session.start_transaction():
                expiring_token_collection.find_and_remove_token_by_user_id(user_id, session)
        except errors.PyMongoError:
            raise TokenDestroyerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.FAILED_TO_DELETE_TOKEN.value)
