import httpx
from constants import *
from exceptions import *


async def request_user_card(user_id: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=f"{USER_MICROSERVICE_URL}/user/{user_id}/card")
            return response.json()
    except Exception:
        raise RecipeException(ErrorCodes.FAILED_TO_GET_USER_CARD.value)
