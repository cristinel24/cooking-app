import httpx
from constants import *
from exceptions import *
from fastapi import status
from schemas import *


async def request_user_card(user_id: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=f"{USER_RETRIEVER_API_URL}/{user_id}/card")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as http_exc:
        status_code = http_exc.response.status_code
        if status_code == status.HTTP_404_NOT_FOUND:
            raise UserRetrieverException(status_code, ErrorCodes.USER_NOT_FOUND)
        else:
            raise UserRetrieverException(status_code, ErrorCodes.FAILED_TO_GET_USER_CARD)
    except Exception:
        raise UserRetrieverException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.FAILED_TO_GET_USER_CARD)

        
async def request_user_cards(user_ids: UserCardRequestData) -> UserCardResponseData:
    async with httpx.AsyncClient() as client:
        payload = user_ids.model_dump_json()
        response = await client.post(url=f"{USER_RETRIEVER_API_URL}/",
                                     content=payload)
        user_card_response_data = UserCardResponseData(cards=[])
        if "cards" not in response.json():
            if "errorCode" in response.json():
                raise RecipeException(int(response.json()["errorCode"]), status.HTTP_404_NOT_FOUND)
            else:
                raise RecipeException(ErrorCodes.NON_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            user_card_response_data.cards = [UserCardData(**card) for card in response.json()["cards"]]
        return user_card_response_data


async def request_recipe_rating(recipe_id: str, x_user_id: str) -> dict | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=f"{RATING_MANAGER_API_URL}", params={"recipe_id": recipe_id, "author_id": x_user_id})
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            if response.status_code == status.HTTP_200_OK:
                return response.json()
    except Exception:
        raise RecipeException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.FAILED_TO_GET_RATING)
