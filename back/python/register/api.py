import constants
import httpx

import exceptions
import schemas
import constants


async def hash_password(password: str, hash_algorithm: str | None, salt: str | None):
    url = f"{constants.HASHER_API_URL}"
    if hash_algorithm:
        url += f"/{hash_algorithm}"
    url += f"/{password}"

    try:
        async with httpx.AsyncClient() as client:
            if salt:
                response = await client.get(url, params={"salt": salt})
            else:
                response = await client.get(url)

            parsed_response = schemas.HasherResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except exceptions.RegisterException as e:
        raise exceptions.RegisterException(error_code=constants.ErrorCodes.PASSWORD_HASHING_FAILED,
                                           status_code=e.status_code)


async def generate_token(user_id: str, token_type: str):
    url = f"{constants.TOKEN_GENERATOR_API_URL}"
    url += f"/{user_id}/{token_type}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            parsed_response = schemas.TokenResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except exceptions.RegisterException as e:
        raise exceptions.RegisterException(error_code=constants.ErrorCodes.TOKEN_GENERATION_FAILED,
                                           status_code=e.status_code)