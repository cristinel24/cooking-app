from constants import ErrorCodes
from repository import DBWrapper
from schemas import UsernameChange
from utils import validate_token_type


def handle_change_username(username_change: UsernameChange):
    if not validate_token_type(username_change.token):
        raise Exception(ErrorCodes.INVALID_TOKEN_TYPE.value)
    db_wrapper = DBWrapper()
    user_id = db_wrapper.get_user_id(username_change.token)
    db_wrapper.update_username(user_id, username_change.username)
    db_wrapper.destroy_tokens(user_id)
