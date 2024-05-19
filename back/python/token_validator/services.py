from constants import TOKEN_TYPES, Errors
from exceptions import TokenException
from fastapi import status
from repository import TokenCollection, UserCollection

token_db = TokenCollection()
user_db = UserCollection()


def get_token(token: str, token_type: str | None = None) -> dict:
    if token_type and token_type not in TOKEN_TYPES:
        raise TokenException(status.HTTP_400_BAD_REQUEST, Errors.INVALID_TYPE)

    response = token_db.get_expiring_token(token, token_type)

    if response is None:
        raise TokenException(status.HTTP_404_NOT_FOUND, Errors.NOT_FOUND)

    to_return = {
        "userId": response["userId"],
        "tokenType": response["tokenType"],
    }

    if to_return["tokenType"] == "session":
        roles = user_db.find_user_roles(to_return["userId"])

        if roles is None:
            raise TokenException(status.HTTP_404_NOT_FOUND, Errors.NOT_FOUND)

        to_return["userRoles"] = roles["roles"]

    return to_return
