from api import request_token_validation, request_token_destroy
from repository import DBWrapper
from schemas import UsernameChange
from utils import validate_request


async def handle_change_username(username_change: UsernameChange):
    validate_request(username_change)
    token_validation_request_response = await request_token_validation(username_change.token)
    await request_token_destroy(token_validation_request_response.userId)
    db_wrapper = DBWrapper()
    db_wrapper.update_username(token_validation_request_response.userId, username_change.username)
