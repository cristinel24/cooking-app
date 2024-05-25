from api import request_password_hash, request_token_validation, request_token_destroy
from repository import DBWrapper
from schemas import PasswordChange


async def handle_change_password(password_change: PasswordChange):
    token_validation_request_response = await request_token_validation(password_change.token)
    hasher_request_response = await request_password_hash(password_change.password)
    await request_token_destroy(token_validation_request_response.userId)
    db_wrapper = DBWrapper()
    db_wrapper.update_password(token_validation_request_response.userId, hasher_request_response.hashAlgorithmName,
                               hasher_request_response.hash, hasher_request_response.salt)
