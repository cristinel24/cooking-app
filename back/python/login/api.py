import httpx

from fastapi import status

from exceptions import LoginException
from schemas import HasherResponse, TokenResponse, UserCardData
from constants import Errors, HASHER_API_URL, TOKEN_GENERATOR_API_URL, USER_RETRIEVER_API_URL


async def request_hash(target: str, alg_name: str, salt: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{HASHER_API_URL}/{alg_name}/{target}?salt={salt}"
            response = await client.get(url=formated_url)
            resp_dict = response.json()
            if resp_dict.get("errorCode") is not None:
                raise LoginException(resp_dict["errorCode"], status.HTTP_503_SERVICE_UNAVAILABLE)
            parsed_response = HasherResponse.model_validate(resp_dict, strict=True)
            return parsed_response  # object of type HasherResponse
    except LoginException as e:
        raise e
    except Exception:
        raise LoginException(Errors.HASH_ERROR, status.HTTP_503_SERVICE_UNAVAILABLE)


async def request_user_card(user_id: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{USER_RETRIEVER_API_URL}/user/{user_id}/card"
            response = await client.get(url=formated_url)
            resp_dict = response.json()
            if resp_dict.get("errorCode") is not None:
                raise LoginException(resp_dict["errorCode"], status.HTTP_503_SERVICE_UNAVAILABLE)
            parsed_response = UserCardData.model_validate(resp_dict, strict=True)
            return parsed_response
    except LoginException as e:
        raise e
    except Exception:
        raise LoginException(Errors.USER_RETRIEVER_ERROR, status.HTTP_503_SERVICE_UNAVAILABLE)


async def request_token(user_id: str, token_type: str):
    try:
        async with httpx.AsyncClient() as client:
            formated_url = f"{TOKEN_GENERATOR_API_URL}/{user_id}/{token_type}"
            response = await client.get(url=formated_url)
            resp_dict = response.json()
            if resp_dict.get("errorCode") is not None:
                raise LoginException(resp_dict["errorCode"], status.HTTP_503_SERVICE_UNAVAILABLE)
            parsed_response = TokenResponse.model_validate(resp_dict, strict=True)
            return parsed_response  # object of type TokenResponse
    except LoginException as e:
        raise e
    except Exception:
        raise LoginException(Errors.TOKEN_ERROR, status.HTTP_503_SERVICE_UNAVAILABLE)