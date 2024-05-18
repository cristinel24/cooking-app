from constants import DESIRED_EMAIL_CHANGE_TOKEN_TYPE
from repository import DBWrapper


def validate_token_type(token: str):
    db_wrapper = DBWrapper()
    return db_wrapper.get_token_type(token) == DESIRED_EMAIL_CHANGE_TOKEN_TYPE
