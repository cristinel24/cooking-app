from api import request_password_hash
from constants import ErrorCodes
from repository import DBWrapper
from schemas import PasswordChange
from utils import validate_token_type


async def handle_change_password(password_change: PasswordChange):
    if not validate_token_type(password_change.token):
        raise Exception(ErrorCodes.INVALID_TOKEN_TYPE.value)
    hasher_request_response = await request_password_hash(password_change.password)
    db_wrapper = DBWrapper()
    user_id = db_wrapper.get_user_id(password_change.token)
    db_wrapper.update_password(user_id, hasher_request_response.hashAlgorithmName, hasher_request_response.hash,
                               hasher_request_response.salt)
    db_wrapper.destroy_tokens(user_id)
