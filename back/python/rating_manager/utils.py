from fastapi import status
from fastapi.responses import JSONResponse
from pymongo import errors

from constants import ErrorCodes, RatingInc
from exception import RecipeRatingManagerException


def transform_exception(e: Exception) -> RecipeRatingManagerException:

    if isinstance(e, RecipeRatingManagerException):
        return e

    if isinstance(e, errors.PyMongoError):

        if e.timeout:
            return RecipeRatingManagerException(
                error_code=ErrorCodes.DB_TIMEOUT.value,
                status_code=status.HTTP_504_GATEWAY_TIMEOUT
            )

        return RecipeRatingManagerException(
            error_code=ErrorCodes.DB_NON_TIMEOUT.value,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return RecipeRatingManagerException(
        error_code=ErrorCodes.UNKNOWN,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def build_response_from_exception(exception: RecipeRatingManagerException) -> JSONResponse:
    return build_response_from_values(exception.status_code, exception.error_code)


def build_response_from_values(status_code: int, error_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"errorCode": error_code})


def get_modify_rating_dict(inc: RatingInc, diff: int) -> dict:
    return {
        "$inc": {
            "ratingCount": inc.value,
            "ratingSum": diff
        }
    }
