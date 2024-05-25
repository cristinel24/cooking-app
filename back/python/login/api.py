import httpx
from constants import (HASHER_API_URL, TOKEN_GENERATOR_API_URL,
                       USER_RETRIEVER_API_URL, Errors)
from exceptions import LoginException
from fastapi import status
from schemas import HasherResponse, TokenResponse, UserCardData


async def request_hash(target: str, alg_name: str, salt: str):
    try:
        async with httpx.AsyncClient() as client:
            formatted_url = f"{HASHER_API_URL}/{alg_name}/{target}?salt={salt}"
            response = await client.get(url=formatted_url)
            resp_dict = response.json()
            if response.status_code != status.HTTP_200_OK:
                raise LoginException(resp_dict.get("errorCode"), response.status_code)
            parsed_response = HasherResponse.model_validate(resp_dict, strict=True)
            return parsed_response  # object of type HasherResponse
    except LoginException as e:
        raise e
    except Exception:
        raise LoginException(Errors.HASH_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)


async def request_user_card(user_id: str):
    try:
        async with httpx.AsyncClient() as client:
            formatted_url = f"{USER_RETRIEVER_API_URL}/{user_id}/card"
            response = await client.get(url=formatted_url)
            resp_dict = response.json()
            if response.status_code != status.HTTP_200_OK:
                raise LoginException(resp_dict.get("errorCode"), response.status_code)
            parsed_response = UserCardData.model_validate(resp_dict, strict=True)
            return parsed_response
    except LoginException as e:
        raise e
    except Exception as e:
        raise LoginException(
            Errors.USER_RETRIEVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def request_token(user_id: str, token_type: str):
    try:
        async with httpx.AsyncClient() as client:
            formatted_url = f"{TOKEN_GENERATOR_API_URL}/{user_id}/{token_type}"
            response = await client.get(url=formatted_url)
            resp_dict = response.json()
            if response.status_code != status.HTTP_200_OK:
                raise LoginException(resp_dict.get("errorCode"), response.status_code)
            parsed_response = TokenResponse.model_validate(resp_dict, strict=True)
            return parsed_response  # object of type TokenResponse
    except LoginException as e:
        raise e
    except Exception as e:
        raise LoginException(Errors.TOKEN_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)
