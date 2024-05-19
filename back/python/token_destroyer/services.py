import os


from repository import *
from constants import ErrorCodes
from exception import TokenDestroyerException
client = MongoCollection()
expiring_token_collection = ExpiringTokenCollection(client.get_connection())
user_collection = UserCollection(client.get_connection())



async def delete_token(token: str):
    session = client.get_connection().start_session()
    try:
        with session.start_transaction():
            token_data = expiring_token_collection.find_and_remove_token(token, session)
            if token_data:
                user_id = token_data.get("userId")
                if token_data.get("tokenType") == "session":
                    user_collection.update_user_field(user_id, "sessions", token_data.get("value"), session)
                elif token_data.get("tokenType") in ["passwordChange", "usernameChange", "emailChange", "emailConfirm"]:
                    user_collection.update_user_field(user_id, "login.changeToken", "None", session)
            else:
                raise TokenDestroyerException(ErrorCodes.TOKEN_NOT_FOUND, 404)
    except TokenDestroyerException as e:
        raise e
    except Exception as e:
        raise TokenDestroyerException(ErrorCodes.FAILED_TO_DELETE_TOKEN, 500) from e
    session.end_session()
