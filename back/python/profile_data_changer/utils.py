from constants import ICON_VALIDATION, DISPLAY_NAME_VALIDATION, DESCRIPTION_VALIDATION, ErrorCodes, ALLOWED_TAGS, ALLOWED_ATTRIBUTES, \
    URL_SCHEMES
from exception import ProfileDataChangerException
from fastapi import status
import nh3


def is_string_sanitized(string: str) -> bool:
    return nh3.clean(html=string, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, url_schemes=URL_SCHEMES) == string


def validate_user_profile_data(data: dict[str, str]) -> None:
    if "icon" in data:
        validate_str(data["icon"], ICON_VALIDATION)
    if "displayName" in data:
        validate_str(data["displayName"], DISPLAY_NAME_VALIDATION)
    if "description" in data:
        validate_str(data["description"], DESCRIPTION_VALIDATION)
        if not is_string_sanitized(data["description"]):
            raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, ErrorCodes.MALFORMED_DESCRIPTION.value)


def validate_str(value: str, checks: dict[str, int]) -> None:
    length = len(value)
    if "required" in checks and length == 0:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["required"])
    if "min_length" in checks and length < checks["min_length"]:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["too_short"])
    if "max_length" in checks and length > checks["max_length"]:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["too_long"])
