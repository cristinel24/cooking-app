import json
import logging

import httpx
from fastapi import status

from constants import *
from exception import RecipeEditorException


async def tokenize_recipe(recipe_data: dict) -> list[str]:
    async with httpx.AsyncClient() as client:
        payload = json.dumps(recipe_data)
        try:
            response = await client.post(url=AI_RECIPE_TOKENIZER_ROUTE,
                                         content=payload)
            if "tags" not in response.json():
                logging.warning("AI API did not return tokens")
                if "errorCode" in response.json():
                    raise RecipeEditorException(int(response.json()["errorCode"]),
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return response.json()["tags"]
        except (Exception,):
            logging.warning("AI API is not responsive")


async def add_allergens(allergens: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"allergens": allergens})
        try:
            response = await client.post(url=INC_ALLERGENS_ROUTE, content=payload)
            if response.status_code <= 199 or response.status_code >= 300:
                if "errorCode" in response.json():
                    raise RecipeEditorException(int(response.json()["errorCode"]),
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Exception,):
            logging.fatal("ALLERGENS MANAGER is not responsive")
            raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def delete_allergens(allergens: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"allergens": allergens})
        try:
            response = await client.post(url=DEC_ALLERGENS_ROUTE, content=payload)
            if response.status_code <= 199 or response.status_code >= 300:
                if "errorCode" in response.json():
                    raise RecipeEditorException(int(response.json()["errorCode"]),
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Exception,):
            raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def add_tags(tags: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"tags": tags})
        try:
            response = await client.post(url=INC_TAGS_ROUTE, content=payload)
            if response.status_code <= 199 or response.status_code >= 300:
                if "errorCode" in response.json():
                    raise RecipeEditorException(int(response.json()["errorCode"]),
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Exception,):
            logging.fatal("TAGS MANAGER is not responsive")
            raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)


async def delete_tags(tags: list[str]):
    async with httpx.AsyncClient() as client:
        payload = json.dumps({"tags": tags})
        try:
            response = await client.post(url=DEC_TAGS_ROUTE, content=payload)
            if response.status_code <= 199 or response.status_code >= 300:
                if "errorCode" in response.json():
                    raise RecipeEditorException(int(response.json()["errorCode"]),
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API,
                                                status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Exception,):
            raise RecipeEditorException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
