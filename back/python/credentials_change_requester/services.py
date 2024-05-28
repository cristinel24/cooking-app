import threading
import asyncio

from constants import ErrorCodes
from exceptions import CredentialChangeRequesterException
from schemas import CredentialChangeRequest
from repository import UserCollection
from constants import USER_DATA_PROJECTION
from api import *
from utils import *

user_collection = UserCollection()


async def create_request(request: CredentialChangeRequest) -> None:
    if not email_validate_function(request.email):
        raise CredentialChangeRequesterException(status.HTTP_400_BAD_REQUEST, ErrorCodes.INVALID_EMAIL.value)

    user = user_collection.get_user_by_email(request.email, USER_DATA_PROJECTION)
    threading.Thread(target=asyncio.run, args=(task(request, user),)).start()


async def task(request: CredentialChangeRequest, user: None | dict):
    if not user:
        return

    token = await request_token(user["id"], request.changeType + "Change")
    
    email_request = ChangeRequest(
        email=request.email,
        token=token,
        changeType=request.changeType
    )

    await send_email(email_request)

