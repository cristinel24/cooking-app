from repository import ExpiringTokenCollection
from repository import UserCollection
from constants import ErrorCodes

expiring_token_collection = ExpiringTokenCollection()
user_collection = UserCollection()


async def delete_token(token: str):
    try:
        token_data = expiring_token_collection.get_expiring_token(token)
        if token_data:
            user_id = token_data.get("userId")
            expiring_token_collection.remove_token(token_data["_id"])
            if token_data.get("tokenType") == "session":
                user_collection.update_user_field(user_id, "sessions", token_data.get("value"))
            elif token_data.get("tokenType") in ["passwordChange", "usernameChange", "emailChange", "emailConfirm"]:
                user_collection.update_user_field(user_id,"login.changeToken", "None")
        else:
            raise Exception(ErrorCodes.TOKEN_NOT_FOUND)
    except Exception as e:
        raise Exception(ErrorCodes.FAILED_TO_DELETE_TOKEN)
