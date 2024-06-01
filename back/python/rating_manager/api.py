import httpx
from fastapi import status
from httpx import Response

from constants import *
from exception import RecipeRatingManagerException
from schemas import *


async def execute_api(method: str, uri: str, json_data: dict | None = None, headers: dict | None = None) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await getattr(client, method)(uri, json=json_data, headers=headers) if json_data \
                else await getattr(client, method)(uri, headers=headers)
            if response.status_code != status.HTTP_200_OK:
                if response.json().get("errorCode") is None:
                    raise RecipeRatingManagerException(
                        error_code=ErrorCodes.UNKNOWN,
                        status_code=status.HTTP_504_GATEWAY_TIMEOUT
                    )
                else:
                    raise RecipeRatingManagerException(
                        error_code=int(response.json()["errorCode"]),
                        status_code=response.status_code
                    )

            return response.json()

    except RecipeRatingManagerException as e:
        raise e
    except (Exception,):
        raise RecipeRatingManagerException(
            error_code=ErrorCodes.UNKNOWN,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def fetch_user_list(user_ids: list[str], x_user_id: str) -> UserCardDataList:
    return UserCardDataList.model_validate(
        await execute_api(
            POST_METHOD, USER_RETRIEVER_API_URL + "/",
            json_data={"ids": user_ids}, headers={"X-User-Id": x_user_id}
        )
    )


async def get_user_card(user_id: str, x_user_id: str) -> UserCardData:
    return UserCardData.model_validate(
        await execute_api(
            GET_METHOD, USER_RETRIEVER_API_URL + f"/{user_id}/card", headers={"X-User-Id": x_user_id}
        )
    )


async def generate_id() -> str:
    return (await execute_api(GET_METHOD, ID_GENERATOR_API_URL + "/"))["id"]
