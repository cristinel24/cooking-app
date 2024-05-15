MAX_TIMEOUT_SECONDS = 3


TOKEN_TYPES = ["session", "usernameChange", "emailChange", "passwordChange", "emailConfirm"]


class Errors:
    INVALID_TYPE = 21603
    DB_ERROR = 21605
    DB_TIMEOUT = 21608
    UNKNOWN = 21609
    NOT_FOUND = 21604
