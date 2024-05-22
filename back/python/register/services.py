from pymongo import errors
from schemas import NewUserData
from repository import UserCollection
from utils import match_collection_error, validate_user_data
from api import *
from datetime import datetime

user_db = UserCollection()


async def register(user_data: NewUserData) -> None:
    user_id = verify_token = None
    try:
        username_exists = user_db.user_exists_by_field("username", user_data.username)
        if username_exists:
            raise RegisterException(status.HTTP_400_BAD_REQUEST, ErrorCodes.USERNAME_ALREADY_EXISTS.value)
        email_exists = user_db.user_exists_by_field("email", user_data.email)
        pending_email_exists = user_db.user_exists_by_field("login.newEmail", user_data.email)
        if email_exists or pending_email_exists:
            raise RegisterException(status.HTTP_400_BAD_REQUEST, ErrorCodes.EMAIL_ALREADY_REGISTERED.value)
        validate_user_data(user_data.__dict__)
        user_id = await request_generate_user_id()
        hash_response = await request_hash(user_data.password)
        new_user_data = {
            "updatedAt": datetime.now(),
            "id": user_id,
            "username": user_data.username,
            "displayName": user_data.displayName or user_data.username,
            "login": {
                "emailStatus": "Pending",
                "hashAlgName": hash_response["hashAlgorithmName"],
                "hash": hash_response["hash"],
                "salt": hash_response["salt"],
                "newEmail": user_data.email
            }
        }
        await user_db.insert_user(new_user_data, EMPTY_USER_DATA)
        verify_token = await request_generate_token(user_id, VERIFY_ACCOUNT_TOKEN_TYPE)
        await request_send_verification_email(user_data.email, verify_token)
    except errors.PyMongoError as e:
        await destroy_data(user_id, verify_token)
        raise match_collection_error(e)
    except RegisterException:
        await destroy_data(user_id, verify_token)
        raise RegisterException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.SERVER_ERROR.value)


async def destroy_data(user_id, verify_token):
    if "user_id" in locals() and user_id:
        await request_destroy_user(user_id)
    if "verify_token" in locals() and verify_token:
        await request_destroy_token(verify_token)
