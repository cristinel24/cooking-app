from constants import ICON_VALIDATION, DISPLAY_NAME_VALIDATION, DESCRIPTION_VALIDATION
from exception import ProfileDataChangerException
from fastapi import status
from html_sanitizer import Sanitizer

sanitizer = Sanitizer()


def sanitize_and_validate_user_profile_data(data: dict[str, str]) -> None:
    # TODO: Sanitize description

    if "icon" in data:
        validate_str(data["icon"], ICON_VALIDATION)
    if "displayName" in data:
        validate_str(data["displayName"], DISPLAY_NAME_VALIDATION)
    if "description" in data:
        data["description"] = sanitizer.sanitize(data["description"])
        validate_str(data["description"], DESCRIPTION_VALIDATION)


def validate_str(value: str, checks: dict[str, int]) -> None:
    length = len(value)
    if "required" in checks and length == 0:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["required"])
    if "min_length" in checks and length < checks["min_length"]:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["too_short"])
    if "max_length" in checks and length > checks["max_length"]:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["too_long"])
