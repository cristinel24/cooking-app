from credentials_change_requester.constants import ErrorCodes
from credentials_change_requester.exceptions import CredentialChangeRequesterException
from schemas import CredentialChangeRequest
from repository import UserCollection
from constants import USER_DATA_PROJECTION
from api import *

user_collection = UserCollection()


async def create_request(request: CredentialChangeRequest) -> dict[str, int]:
    try:
        user = user_collection.get_user_by_email(request.email, USER_DATA_PROJECTION)
        if not user:
            raise CredentialChangeRequesterException(status.HTTP_404_NOT_FOUND, ErrorCodes.USER_NOT_FOUND)
        try:
            token = await request_token(user["id"], request.changeType + "Change")
        except Exception as e:
            raise CredentialChangeRequesterException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.TOKEN_GENERATION_ERROR)
        email_request = ChangeRequest(
            email=request.email,
            token=token["value"],
            changeType=request.changeType
        )
        try:
            await send_email(email_request)
        except Exception as e:
            raise CredentialChangeRequesterException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.EMAIL_SEND_ERROR)
    except CredentialChangeRequesterException as e:
        raise e
    return {"errorCode": 200}
