import pymongo

from exceptions import TokenException, UserException
from repository import UserCollection, TokenCollection
from constants import TOKEN_TYPES, Errors
from utils import generate_token
from fastapi import status


user_db = UserCollection()
token_db = TokenCollection()


def insert_user_token(user_id: str, token_type: str) -> dict:
    if token_type not in TOKEN_TYPES:
        raise TokenException(status.HTTP_400_BAD_REQUEST, Errors.INVALID_TYPE)

    if not user_db.exists_user(user_id):
        raise UserException(status.HTTP_404_NOT_FOUND, Errors.USER_NOT_FOUND)

    try:
        value = generate_token()
        while token_db.exists_token(value):
            value = generate_token()
        token = token_db.insert_token(value, user_id, token_type)
        return token
    # Eroare cu Mongo, returnam internal server error
    except pymongo.errors.PyMongoError.timeout:
        raise TokenException(status.HTTP_500_INTERNAL_SERVER_ERROR, Errors.DB_TIMEOUT)
