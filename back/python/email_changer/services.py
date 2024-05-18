from api import request_token_generation, request_account_verification
from constants import ErrorCodes
from repository import DBWrapper
from schemas import EmailChange
from utils import validate_token_type


async def handle_change_email(email_change: EmailChange):
    if not validate_token_type(email_change.token):
        raise Exception(ErrorCodes.INVALID_TOKEN_TYPE.value)
    db_wrapper = DBWrapper()
    user_id = db_wrapper.get_user_id(email_change.token)
    db_wrapper.update_email(user_id, email_change.email)
    db_wrapper.destroy_tokens(user_id)
    token_generation_request_result = await request_token_generation(user_id, "emailConfirm")
    await request_account_verification(email_change.email, token_generation_request_result.value)
