import json
import logging

import httpx
from fastapi import status

from constants import ErrorCodes, ID_GENERATOR_ROUTE, ID_GENERATOR_API_URL, AI_API_URL, AI_RECIPE_TOKENIZER_ROUTE
from exception import RecipeCreatorException


async def get_id() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=ID_GENERATOR_API_URL + ID_GENERATOR_ROUTE)
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
            response = await client.post(url=AI_API_URL + AI_RECIPE_TOKENIZER_ROUTE,
                                         content=payload)
        except httpx.ConnectError:
            logging.warning("\tAI API IS NOT RESPONSIVE")
        if response.json().get("tokens") is None:
            logging.warning("\tAI API DID NOT RETURN TOKENS")
        else:
            return response.json()["tokens"]


async def add_allergens(allergens: list[str]):
    pass


async def delete_allergens(allergens: list[str]):
    pass


async def add_tags(tags: list[str]):
    pass


async def delete_tags(tags: list[str]):
    pass
