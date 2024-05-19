from fastapi import status
from exception import TokenDestroyerException
from repository import *

client = MongoCollection()
user_collection = UserCollection(client.get_connection())
expiring_token_collection = ExpiringTokenCollection(client.get_connection())


async def delete_token(token: str):
    token_data = expiring_token_collection.find_and_remove_token(token)

    if not token_data:
        raise TokenDestroyerException(
            status.HTTP_404_NOT_FOUND, ErrorCodes.TOKEN_NOT_FOUND.value
        )


async def delete_user_tokens(user_id: str):
    if not user_collection.exists_user(user_id):
        raise TokenDestroyerException(
            status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND.value
        )

    expiring_token_collection.find_and_remove_token_by_user_id(user_id)
