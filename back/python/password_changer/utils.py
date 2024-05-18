from constants import DESIRED_PASSWORD_CHANGE_TOKEN_TYPE
from repository import DBWrapper


def validate_token_type(token: str):
    db_wrapper = DBWrapper()
    return db_wrapper.get_token_type(token) == DESIRED_PASSWORD_CHANGE_TOKEN_TYPE
