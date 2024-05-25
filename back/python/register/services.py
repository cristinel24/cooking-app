import logging
from pymongo import errors
from schemas import NewUserData
from repository import UserCollection, MongoCollection
from utils import match_collection_error, validate_user_data, run_async_in_thread
from api import *
from datetime import datetime

client = MongoCollection()
user_collection = UserCollection(client.connection)


async def register(user_data: NewUserData) -> None:
    user_id = None
    try:
        fields = [
            {"username": user_data.username},
            {"email": user_data.email},
            {"login.newEmail": user_data.email}
        ]
        user = user_collection.user_exists_by_fields(fields)
        if user is not None:
            if "username" in user and user["username"] == user_data.username:
                raise RegisterException(status.HTTP_400_BAD_REQUEST, ErrorCodes.USERNAME_EXISTS.value)
            if (("email" in user and user["email"] == user_data.email) or
                    ("login" in user and "newEmail" in user["login"] and user["login"]["newEmail"] == user_data.email)):
                logging.warning(f"Email {user_data.email} already exists")
                return None

        validate_user_data(vars(user_data))
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
        run_async_in_thread(create_account_thread, new_user_data, user_id, user_data.email)
    except errors.PyMongoError as e:
        await destroy_data(user_id)
        raise match_collection_error(e)
    except RegisterException as e:
        await destroy_data(user_id)
        raise RegisterException(e.status_code, e.error_code)


async def create_account_thread(new_user_data: dict, user_id: str, email: str) -> None:
    verify_token = None
    try:
        user_collection.insert_user(new_user_data, EMPTY_USER_DATA)
        verify_token = await request_generate_token(user_id, VERIFY_ACCOUNT_TOKEN_TYPE)
        await request_send_verification_email(email, verify_token)
    except (Exception,) as e:
        await request_destroy_user(new_user_data["id"])
        logging.error(f"Error while creating account: {e}: {vars(e)}")


async def destroy_data(user_id):
    if user_id is not None:
        await request_destroy_user(user_id)
