from constants import *
from schemas import AccountVerification, ChangeRequest
from utils import send_email


def handle_account_verification(request_data: AccountVerification):
    with open(os.path.join(TEMPLATES_DIR_PATH, ACCOUNT_VERIFICATION_FILE_NAME), "rt", encoding="utf8") as fp:
        email_template = fp.read()
    verification_link = f"{COOKING_APP_DOMAIN}/{ACCOUNT_VERIFICATION_ROUTE}/{request_data.token}"
    email_body = email_template.format(email_address=request_data.email, verification_link=verification_link)
    send_email(request_data.email, ACCOUNT_VERIFICATION_SUBJECT, email_body)


def handle_change_request(request_data: ChangeRequest):
    with open(os.path.join(TEMPLATES_DIR_PATH, CHANGE_REQUEST_FILE_NAME), "rt", encoding="utf8") as fp:
        email_template = fp.read()
    verification_link = f"{COOKING_APP_DOMAIN}/{CHANGE_REQUEST_ROUTE}/{request_data.token}"
    email_body = email_template.format(email_address=request_data.email, change_resource=request_data.changeType,
                                       verification_link=verification_link)
    send_email(request_data.email, CHANGE_REQUEST_SUBJECT, email_body)
