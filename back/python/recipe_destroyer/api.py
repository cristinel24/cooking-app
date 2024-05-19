from constants import *
import httpx
from fastapi import status
from exception import *


async def delete_allergens(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RECIPE_RETRIEVER_ALLERGENS_API_URL}/allergen/{name}")
        
        if response.status_code != 200:
             if response.json().get("errorCode") is None:
                raise RecipeDestroyerException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
             else:
                raise RecipeDestroyerException(int(response.json()["errorCode"]), status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return response.status_code
        
async def delete_ratings(rating_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RECIPE_RETRIEVER_RATINGS_API_URL}/rating/{rating_id}")
        
        if response.status_code != 200:
             if response.json().get("errorCode") is None:
                raise RecipeDestroyerException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
             else:
                raise RecipeDestroyerException(int(response.json()["errorCode"]), status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return response.status_code
    
async def delete_tags(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RECIPE_RETRIEVER_TAGS_API_URL}/tag/{name}")

        if response.status_code != 200:
             if response.json().get("errorCode") is None:
                raise RecipeDestroyerException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
             else:
                raise RecipeDestroyerException(int(response.json()["errorCode"]), status.HTTP_500_INTERNAL_SERVER_ERROR) 
        return response.status_code
    

async def delete_image(image_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{RECIPE_RETRIEVER_IMAGES_API_URL}/{image_id}")

        if response.status_code != 200:
             if response.json().get("errorCode") is None:
                raise RecipeDestroyerException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
             else:
                raise RecipeDestroyerException(int(response.json()["errorCode"]), status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response.status_code