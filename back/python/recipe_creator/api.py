import json

import httpx
from fastapi import status

from constants import *
from exception import RecipeCreatorException
import logging


async def get_id() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=ID_GENERATOR_ROUTE)
        if response.json().get("id") is None:
            if response.json().get("errorCode") is None:
                raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                raise RecipeCreatorException(int(response.json()["errorCode"]), status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return response.json()["id"]


async def tokenize_recipe(recipe_data: dict) -> list[str]:
    async with httpx.AsyncClient() as client:
        payload = json.dumps(recipe_data)
        try:
            response = await client.post(url=AI_RECIPE_TOKENIZER_ROUTE,
                                         content=payload)
        except httpx.ConnectError:
            logging.warning("AI API is not responsive")
        if response.json().get("tokens") is None:
            logging.warning("AI API did not return tokens")
        else:
            return response.json()["tokens"]


async def add_allergens(allergens: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"allergens": allergens})
        try:
            await client.post(url=ADD_ALLERGENS_ROUTE, content=payload)
        except (Exception,):
            logging.fatal("ALLERGENS MANAGER is not responsive")
            raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def delete_allergens(allergens: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"allergens": allergens})
        try:
            await client.patch(url=DELETE_ALLERGENS_ROUTE, content=payload)
        except (Exception,):
            raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def add_tags(tags: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"tags": tags})
        try:
            await client.post(url=ADD_TAGS_ROUTE, content=payload)
        except (Exception,):
            logging.fatal("TAGS MANAGER is not responsive")
            raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def delete_tags(tags: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"tags": tags})
        try:
            await client.patch(url=DELETE_TAGS_ROUTE, content=payload)
        except (Exception,):
            raise RecipeCreatorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
