import json
import os
import httpx
from constants import ErrorCodes
from schemas import TokenGeneratorRequestResponse


async def request_token_generation(user_id: str, token_type: str) -> TokenGeneratorRequestResponse:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{os.getenv('TOKEN_GENERATOR_API_URL', 'http://localhost:8090')}/{user_id}/{token_type}"
            response = await client.get(url=request_url)
            parsed_response = TokenGeneratorRequestResponse.model_validate(response.json(), strict=True)
            return parsed_response
    except Exception:
        raise Exception(ErrorCodes.TOKEN_GENERATION_REQUEST_FAILED.value)


async def request_account_verification(email: str, token: str) -> None:
    try:
        async with httpx.AsyncClient() as client:
            request_url = f"{os.getenv('EMAIL_SYSTEM_API_URL', 'http://localhost:2060')}/verify-account"
            response = await client.post(url=request_url, content=json.dumps({"email": email, "token": token}))
            if response.json() is not None:
                raise Exception()
    except Exception:
        raise Exception(ErrorCodes.ACCOUNT_VERIFICATION_REQUEST_FAILED.value)
