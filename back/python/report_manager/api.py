import httpx
from fastapi import status
from httpx import Response

from constants import *
from exception import ReportManagerException
from schemas import *


async def execute_api(method: str, uri: str, json_data: dict | None = None) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await getattr(client, method)(uri, json=json_data) if json_data \
                else await getattr(client, method)(uri)
            if response.status_code != status.HTTP_200_OK:
                if response.json().get("errorCode") is None:
                    raise ReportManagerException(
                        error_code=ErrorCodes.UNKNOWN,
                        status_code=status.HTTP_504_GATEWAY_TIMEOUT
                    )
                else:
                    raise ReportManagerException(
                        error_code=int(response.json()["errorCode"]),
                        status_code=response.status_code
                    )

            return response.json()

    except ReportManagerException as e:
        raise e
    except (Exception,):
        raise ReportManagerException(
            error_code=ErrorCodes.UNKNOWN,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_user_card(user_id: str) -> UserCardData:
    return UserCardData.model_validate(
        await execute_api(
            GET_METHOD, USER_RETRIEVER_API_URL + f"/{user_id}/card"
        )
    )


async def get_recipe_data(recipe_id: str) -> RecipeData:
    return RecipeData.model_validate(
        await execute_api(
            GET_METHOD, RECIPE_RETRIEVER_API_URL + f"/{recipe_id}"
        )
    )


async def get_user_data(user_id: str) -> UserData:
    return UserData.model_validate(
        await execute_api(
            GET_METHOD, USER_RETRIEVER_API_URL + f"/{user_id}"
        )
    )


async def get_rating_data_card(recipe_id: str) -> RatingDataCard:
    return RatingDataCard.model_validate(
        await execute_api(
            GET_METHOD, RATING_MANAGER_API_URL + f"/{recipe_id}/card"
        )
    )
