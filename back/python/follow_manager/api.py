import httpx
from fastapi import status

from constants import USER_RETRIEVER_API_URL
from exception import FollowManagerException
from schemas import *


async def request_user_cards(user_ids: UserCardRequestData) -> UserCardResponseData:
    async with httpx.AsyncClient() as client:
        payload = user_ids.model_dump_json()
        response = await client.post(url=USER_RETRIEVER_API_URL,
                                     content=payload)
        user_card_response_data = UserCardResponseData(cards=[])
        if response.json().get("cards") is None:
            raise FollowManagerException(int(response.json()["errorCode"]), status.HTTP_404_NOT_FOUND)
        else:
            user_card_response_data.cards = [UserCardData(**card) for card in response.json()["cards"]]
        return user_card_response_data
