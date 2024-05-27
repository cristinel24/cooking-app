from constants import *
from schemas import AccountVerification, ChangeRequest
from utils import send_email, validate_email


def handle_account_verification(request_data: AccountVerification):
    if not validate_email(request_data.email):
        raise Exception(ErrorCodes.INVALID_EMAIL_PROVIDED.value)
    try:
        with open(os.path.join(TEMPLATES_DIR_PATH, ACCOUNT_VERIFICATION_FILE_NAME), "rt", encoding="utf8") as fp:
            email_template = fp.read()
    except Exception as e:
        raise Exception(ErrorCodes.ACCOUNT_VERIFICATION_TEMPLATE_READING_FAILED.value)
    verification_link = f"{FRONTEND_URL}/{ACCOUNT_VERIFICATION_ROUTE}?token={request_data.token}"
    try:
        email_body = email_template.format(email_address=request_data.email, verification_link=verification_link)
    except Exception as e:
        raise Exception(ErrorCodes.ACCOUNT_VERIFICATION_TEMPLATE_FORMATTING_FAILED.value)
    send_email(request_data.email, ACCOUNT_VERIFICATION_SUBJECT, email_body)


def handle_change_request(request_data: ChangeRequest):
    if not validate_email(request_data.email):
        raise Exception(ErrorCodes.INVALID_EMAIL_PROVIDED.value)
    try:
        with open(os.path.join(TEMPLATES_DIR_PATH, CHANGE_REQUEST_FILE_NAME), "rt", encoding="utf8") as fp:
            email_template = fp.read()
    except Exception as e:
        raise Exception(ErrorCodes.REQUEST_CHANGE_TEMPLATE_READING_FAILED.value)
    verification_link = f"{FRONTEND_URL}/{CHANGE_REQUEST_ROUTE}/{request_data.token}"
    try:
        email_body = email_template.format(email_address=request_data.email, change_resource=request_data.changeType,
                                           verification_link=verification_link)
    except Exception as e:
        raise Exception(ErrorCodes.REQUEST_CHANGE_TEMPLATE_FORMATTING_FAILED.value)
    send_email(request_data.email, CHANGE_REQUEST_SUBJECT, email_body)
