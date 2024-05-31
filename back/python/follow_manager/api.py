import httpx
from fastapi import status

from constants import USER_RETRIEVER_API_URL, USER_CARDS_ROUTE, ErrorCodes
from exception import FollowManagerException
from schemas import *


async def request_user_cards(user_ids: UserCardRequestData, x_user_id: str) -> UserCardResponseData:
    async with httpx.AsyncClient() as client:
        payload = user_ids.model_dump_json()
        response = await client.post(url=USER_RETRIEVER_API_URL + USER_CARDS_ROUTE,
                                     content=payload, headers={"x-user-id": x_user_id})
        user_card_response_data = UserCardResponseData(cards=[])
        if "cards" not in response.json():
            if "errorCode" in response.json():
                raise FollowManagerException(int(response.json()["errorCode"]), status.HTTP_404_NOT_FOUND)
            else:
                raise FollowManagerException(ErrorCodes.NOT_RESPONSIVE_API.value, status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            user_card_response_data.cards = [UserCardData(**card) for card in response.json()["cards"]]
        return user_card_response_data
