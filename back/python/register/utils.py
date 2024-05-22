from pymongo import errors
from exception import RegisterException
from constants import *
from fastapi import status
import re


def match_collection_error(e: errors.PyMongoError) -> RegisterException:
    if e.timeout:
        return RegisterException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, error_code=ErrorCodes.DATABASE_TIMEOUT.value)
    else:
        return RegisterException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_code=ErrorCodes.DATABASE_ERROR.value)


def validate_user_data(data: dict) -> None:
    if "displayName" in data and data["displayName"] is not None:
        validate_str(data["displayName"], DISPLAY_NAME_VALIDATION)
    validate_str(data["username"], USERNAME_VALIDATION)
    validate_str(data["email"], EMAIL_VALIDATION)
    validate_str(data["password"], PASSWORD_VALIDATION)


def validate_str(value: str, checks: dict) -> None:
    length = len(value)
    if "required" in checks and length == 0:
        raise RegisterException(status.HTTP_400_BAD_REQUEST, checks["required"])
    if "min_length" in checks and length < checks["min_length"]:
        raise RegisterException(status.HTTP_400_BAD_REQUEST, checks["too_short"])
    if "max_length" in checks and length > checks["max_length"]:
        raise RegisterException(status.HTTP_400_BAD_REQUEST, checks["too_long"])
    if "pattern" in checks and not re.fullmatch(checks["pattern"]["regex"], value):
        raise RegisterException(status.HTTP_400_BAD_REQUEST, checks["pattern"]["error"])
