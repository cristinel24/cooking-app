import httpx
from fastapi import status
from httpx import Response

from constants import *
from exception import *


async def execute_api(method: str, uri: str, json_data: dict | None = None) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await getattr(client, method)(uri, json=json_data) if json_data \
                else await getattr(client, method)(uri)
            if response.status_code != status.HTTP_200_OK:
                if response.json().get("errorCode") is None:
                    raise RecipeDestroyerException(error_code=ErrorCodes.NOT_RESPONSIVE_API,
                                                   status_code=status.HTTP_504_GATEWAY_TIMEOUT)
                else:
                    raise RecipeDestroyerException(error_code=int(response.json()["errorCode"]),
                                                   status_code=response.status_code)

            return response.json()

    except RecipeDestroyerException as e:
        raise e
    except (Exception,):
        raise RecipeDestroyerException(error_code=ErrorCodes.SERVER_ERROR,
                                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def delete_allergens(allergens: list[str]):
    await execute_api(POST_METHOD, DEC_ALLERGENS_ROUTE, {"allergens": allergens})


async def add_allergens(allergens: list[str]):
    await execute_api(POST_METHOD, INC_ALLERGENS_ROUTE, {"allergens": allergens})


async def delete_tags(tags: list[str]):
    await execute_api(POST_METHOD, DEC_TAGS_ROUTE, {"tags": tags})


async def add_tags(tags: list[str]):
    await execute_api(POST_METHOD, INC_TAGS_ROUTE, {"tags": tags})


async def delete_rating(rating_id: str):
    await execute_api(DELETE_METHOD, RATING_MANAGER_API_URL + f"/{rating_id}")


async def delete_image(image_id: str):
    await execute_api(DELETE_METHOD, IMAGE_STORAGE_API_URL + f"/{image_id}")


async def retrieve_recipe(recipe_id: str) -> dict:
    return await execute_api(GET_METHOD, RECIPE_RETRIEVE_ROUTE.format(recipe_id=recipe_id))
