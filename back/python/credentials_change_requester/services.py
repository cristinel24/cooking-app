from constants import ErrorCodes
from exceptions import CredentialChangeRequesterException
from schemas import CredentialChangeRequest
from repository import UserCollection
from constants import USER_DATA_PROJECTION
from api import *
from utils import *

user_collection = UserCollection()


async def create_request(request: CredentialChangeRequest) -> None:
    if email_validate_function(request.email):
        user = user_collection.get_user_by_email(request.email, USER_DATA_PROJECTION)
    else:
        raise CredentialChangeRequesterException(status.HTTP_400_BAD_REQUEST, ErrorCodes.INVALID_EMAIL.value)
    try:
        token = await request_token(user["id"], request.changeType + "Change")
    except httpx.ConnectError:
        raise CredentialChangeRequesterException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                 ErrorCodes.TOKEN_GENERATION_ERROR.value)
    email_request = ChangeRequest(
        email=request.email,
        token=token,
        changeType=request.changeType
    )
    try:
        await send_email(email_request)
    except httpx.ConnectError:
        raise CredentialChangeRequesterException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                 ErrorCodes.EMAIL_SEND_ERROR.value)