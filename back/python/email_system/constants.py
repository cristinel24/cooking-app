import os

COOKING_APP_DOMAIN = "https://cooking.app"
ACCOUNT_VERIFICATION_ROUTE = "verify_account"
CHANGE_REQUEST_ROUTE = "verify_change"

TEMPLATES_DIR_PATH = os.path.join(os.path.dirname(__file__), "templates")
ACCOUNT_VERIFICATION_FILE_NAME = "account_verification.html"
CHANGE_REQUEST_FILE_NAME = "change_request.html"

ACCOUNT_VERIFICATION_SUBJECT = "Account Verification Requested"
CHANGE_REQUEST_SUBJECT = "Account Change Requested"
