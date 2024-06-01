from api import request_token_generation, request_email_verification, request_token_validation, request_token_destroy
from constants import EMAIL_VERIFICATION_TOKEN_TYPE, ErrorCodes
from repository import DBWrapper
from schemas import EmailChange
from utils import validate_request


async def handle_change_email(email_change: EmailChange):
    validate_request(email_change)
    db_wrapper = DBWrapper()
    if not db_wrapper.check_unique_email(email_change.email):
        raise Exception(ErrorCodes.EMAIL_UNIQUE_CONSTRAINT_VIOLATED.value)
    token_validation_request_response = await request_token_validation(email_change.token)
    await request_token_destroy(token_validation_request_response.userId)
    token_generation_request_response = await request_token_generation(token_validation_request_response.userId,
                                                                       EMAIL_VERIFICATION_TOKEN_TYPE)
    await request_email_verification(email_change.email, token_generation_request_response.value)
    db_wrapper.update_email(token_validation_request_response.userId, email_change.email)
