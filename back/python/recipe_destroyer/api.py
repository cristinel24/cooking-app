import httpx
from fastapi import status
from httpx import Response

from constants import *
from exception import *
from utils import logger


async def execute_api(method: str, uri: str, json_data: dict | None = None, headers: dict | None = None) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await getattr(client, method)(uri, json=json_data, headers=headers) if json_data \
                else await getattr(client, method)(uri, headers=headers)
            if response.status_code != status.HTTP_200_OK:
                if response.json().get("errorCode") is None:
                    raise RecipeDestroyerException(
                        error_code=ErrorCodes.NOT_RESPONSIVE_API,
                        status_code=status.HTTP_504_GATEWAY_TIMEOUT
                    )
                else:
                    raise RecipeDestroyerException(
                        error_code=int(response.json()["errorCode"]),
                        status_code=response.status_code
                    )

            return response.json()

    except RecipeDestroyerException as e:
        raise e
    except (Exception,) as e:
        logger.error(e)
        raise RecipeDestroyerException(
            error_code=ErrorCodes.SERVER_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def post_allergens(allergens: list[str], action: int):
    await execute_api(POST_METHOD, f"{POST_ALLERGENS_ROUTE}?action={action}", {"allergens": allergens})


async def post_tags(tags: list[str], action: int):
    await execute_api(POST_METHOD, f"{POST_TAGS_ROUTE}?action={action}", {"tags": tags})


async def delete_ratings(rating_id: str, author_id: str):
    await execute_api(DELETE_METHOD, DELETE_RATINGS_ROUTE.format(id=rating_id), headers={"X-User-Id": author_id})


async def delete_image(image_id: str):
    await execute_api(DELETE_METHOD, IMAGE_STORAGE_API_URL + f"/{image_id}")


async def retrieve_recipe(recipe_id: str) -> dict:
    return await execute_api(GET_METHOD, RECIPE_RETRIEVE_ROUTE.format(recipe_id=recipe_id))
