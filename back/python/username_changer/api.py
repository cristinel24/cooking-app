import httpx
from constants import ErrorCodes, TOKEN_VALIDATOR_API_URL, DESIRED_USERNAME_CHANGE_TOKEN_TYPE, TOKEN_DESTROYER_API_URL
from schemas import TokenValidatorRequestResponse


async def request_token_validation(token: str) -> TokenValidatorRequestResponse:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{TOKEN_VALIDATOR_API_URL}/{DESIRED_USERNAME_CHANGE_TOKEN_TYPE}/{token}"
            response = await client.get(url=request_url)
            parsed_response = TokenValidatorRequestResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise Exception(ErrorCodes.TOKEN_VALIDATOR_REQUEST_FAILED.value)


async def request_token_destroy(user_id: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{TOKEN_DESTROYER_API_URL}/{user_id}/tokens"
            response = await client.delete(url=request_url)
            if response.json() is not None:
                raise Exception()
    except Exception:
        raise Exception(ErrorCodes.TOKEN_DESTROYER_REQUEST_FAILED.value)
