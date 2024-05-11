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
            user = user_collection.get_user_by_id(user_id)
            expiring_token_collection.remove_token(token_data["_id"])
            if token_data.get("tokenType") == "session":
                sessions = user["sessions"]
                for session in sessions:
                    if session.get("value") == token_data.get("value"):
                        sessions.remove(session)
                        break
            elif token_data.get("tokenType") in ["passwordChange", "usernameChange", "emailChange"]:
                user["login"]["changeToken"] = None
            user_collection.update_user(user)
            return {"Token deleted successfully"}
        else:
            raise Exception(ErrorCodes.TOKEN_NOT_FOUND)
    except Exception as e:
        raise Exception(ErrorCodes.FAILED_TO_DELETE_TOKEN)
