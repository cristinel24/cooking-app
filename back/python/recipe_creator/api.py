import json
import logging

import httpx
from fastapi import status

from constants import *
from exception import RecipeCreatorException


async def get_id() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=ID_GENERATOR_ROUTE)
        if "id" not in response.json():
            if "errorCode" in response.json():
                raise RecipeCreatorException(int(response.json()["errorCode"]),
                                             status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API,
                                             status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response.json()["id"]


async def tokenize_recipe(recipe_data: dict) -> list[str]:
    async with httpx.AsyncClient() as client:
        payload = json.dumps(recipe_data)
        try:
            response = await client.post(url=AI_RECIPE_TOKENIZER_ROUTE,
                                         content=payload)
            if "tokens" not in response.json():
                logging.warning("AI API did not return tokens")
                if "errorCode" in response.json():
                    raise RecipeCreatorException(int(response.json()["errorCode"]),
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return response.json()["tokens"]
        except (Exception,):
            logging.warning("AI API is not responsive")


async def post_allergens(allergens: list[str], action: int):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"allergens": allergens})
        try:
            response = await client.post(url=f"{POST_ALLERGENS_ROUTE}?action={action}", content=payload)
            if response.status_code <= 199 or response.status_code >= 300:
                if "errorCode" in response.json():
                    raise RecipeCreatorException(int(response.json()["errorCode"]),
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Exception,):
            logging.fatal("ALLERGENS MANAGER is not responsive")
            raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def post_tags(tags: list[str], action: int):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"tags": tags})
        try:
            response = await client.post(url=f"{POST_TAGS_ROUTE}?action={action}", content=payload)
            if response.status_code <= 199 or response.status_code >= 300:
                if "errorCode" in response.json():
                    raise RecipeCreatorException(int(response.json()["errorCode"]),
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                 status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Exception,):
            logging.fatal("TAGS MANAGER is not responsive")
            raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
