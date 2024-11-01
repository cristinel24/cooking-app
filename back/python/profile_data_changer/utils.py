from constants import *
from exception import ProfileDataChangerException
from fastapi import status
from pymongo import errors
import nh3


class Actions:
    INCREMENT = 1
    DECREMENT = -1


def sanitize_html(fields: dict[str, str | list[str]]) -> dict[str, str | list[str]]:
    clean_fields = dict()
    for key, value in fields.items():
        if isinstance(value, list):
            clean_htmls = list()
            for item in value:
                clean_htmls.append(
                    nh3.clean(html=item, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, url_schemes=URL_SCHEMES))
                if not clean_htmls[-1]:
                    raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, ErrorCodes.MALFORMED_HTML.value)
            clean_fields[key] = clean_htmls
        elif isinstance(value, str):
            clean_fields[key] = nh3.clean(html=value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
                                          url_schemes=URL_SCHEMES)
            if not clean_fields[key]:
                raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, ErrorCodes.MALFORMED_HTML.value)
    return clean_fields


def validate_user_profile_data(data: dict[str, str]) -> None:
    if "icon" in data:
        validate_str(data["icon"], ICON_VALIDATION)
    if "displayName" in data:
        validate_str(data["displayName"], DISPLAY_NAME_VALIDATION)
    if "description" in data:
        validate_str(data["description"], DESCRIPTION_VALIDATION)


def validate_str(value: str, checks: dict[str, int]) -> None:
    length = len(value)
    if "required" in checks and length == 0:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["required"])
    if "min_length" in checks and length < checks["min_length"]:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["too_short"])
    if "max_length" in checks and length > checks["max_length"]:
        raise ProfileDataChangerException(status.HTTP_400_BAD_REQUEST, checks["too_long"])


def match_collection_error(e: errors.PyMongoError) -> ProfileDataChangerException:
    if e.timeout:
        return ProfileDataChangerException(status.HTTP_504_GATEWAY_TIMEOUT, ErrorCodes.DATABASE_TIMEOUT.value)
    return ProfileDataChangerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)
