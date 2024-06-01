import re
from constants import TOKEN_VALIDATION, PASSWORD_VALIDATION
from schemas import PasswordChange


def validate_str(value: str, checks: dict) -> None:
    length = len(value)
    if "required" in checks and length == 0:
        raise Exception(checks["required"])
    if "min_length" in checks and length < checks["min_length"]:
        raise Exception(checks["too_short"])
    if "max_length" in checks and length > checks["max_length"]:
        raise Exception(checks["too_long"])
    if "pattern" in checks and not re.fullmatch(checks["pattern"]["regex"], value):
        raise Exception(checks["pattern"]["error"])


def validate_request(request: PasswordChange) -> None:
    validate_str(request.token, TOKEN_VALIDATION)
    validate_str(request.password, PASSWORD_VALIDATION)
