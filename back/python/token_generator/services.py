import pymongo

from exceptions import TokenException
from repository import TokenCollection
from constants import TOKEN_TYPES, Errors, MAX_TIMEOUT_SECONDS
from utils import generate_token
from pymongo import errors

token_db = TokenCollection()


def insert_user_token(user_id: str, token_type: str) -> dict:
    if token_type not in TOKEN_TYPES:
        raise TokenException(Errors.INVALID_TYPE)
    try:
        value = generate_token()
        while token_db.exists_token(value):
            value = generate_token()
        token = token_db.insert_token(value, user_id, token_type)
        return token
    # Eroare cu Mongo, returnam internal server error
    except pymongo.errors.PyMongoError.timeout as e:
        raise TokenException(Errors.DB_TIMEOUT)
    except TokenException as e:
        raise e
