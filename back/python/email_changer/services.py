from api import request_token_generation, request_email_verification, request_token_validation, request_token_destroy
from constants import EMAIL_VERIFICATION_TOKEN_TYPE
from repository import DBWrapper
from schemas import EmailChange


async def handle_change_email(email_change: EmailChange):
    token_validation_request_response = await request_token_validation(email_change.token)
    await request_token_destroy(token_validation_request_response.userId)
    token_generation_request_response = await request_token_generation(token_validation_request_response.userId,
                                                                       EMAIL_VERIFICATION_TOKEN_TYPE)
    await request_email_verification(email_change.email, token_generation_request_response.value)
    db_wrapper = DBWrapper()
    db_wrapper.update_email(token_validation_request_response.userId, email_change.email)
