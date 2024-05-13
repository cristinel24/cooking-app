from enum import Enum


class EmailStatus(Enum):
    PENDING = "Pending"
    TRANSITIONING = "Transitioning"
    CONFIRMED = "Confirmed"


class ExpiringTokenType(Enum):
    SESSION = "session"
    USERNAME_CHANGE = "usernameChange"
    EMAIL_CHANGE = "emailChange"
    PASSWORD_CHANGE = "passwordChange"
    EMAIL_CONFIRM = "emailConfirm"
