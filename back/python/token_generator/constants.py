TOKEN_TYPES = ["session", "usernameChange", "emailChange", "passwordChange", "emailConfirm"]

MAX_TIMEOUT_SECONDS = 3


class Errors:
    USER_NOT_FOUND = 20404
    INVALID_TYPE = 20400
    DATABASE_ERROR = 20405
    DB_TIMEOUT = 20413
