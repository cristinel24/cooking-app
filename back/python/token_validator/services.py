from exceptions import TokenException
from repository import TokenCollection, UserCollection
from constants import TOKEN_TYPES, Errors


token_db = TokenCollection()
user_db = UserCollection()


def token_is_valid(token_value: str, token_type: str) -> dict:
    try:
        if token_type not in TOKEN_TYPES:
            raise TokenException(Errors.INVALID_TYPE)
        response = token_db.get_expiring_token(token_value, token_type)
        if response is None:
            raise TokenException(Errors.NOT_FOUND)
        to_return = {
            "userId": response["userId"],
        }
        if token_type == "session":
            roles = user_db.find_user_roles(response["userId"])
            to_return["userRoles"] = roles
        return to_return
    except (Exception,) as e:
        raise e


def get_token(token_value: str) -> dict:
    try:
        response = token_db.get_expiring_token(token_value)
        if response is None:
            raise TokenException(Errors.NOT_FOUND)
        return {
            "userId": response["userId"],
            "type": response["tokenType"]
        }
    except (Exception,) as e:
        raise e

