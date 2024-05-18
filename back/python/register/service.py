import pymongo.errors

from constants import ErrorCodes
from schemas import UserCreateData
from exceptions import RegisterException
from repository import UserCollection
from api import hash_password, generate_token

user_db = UserCollection()

async def register(user_data: UserCreateData) -> dict:
    try:
        username = user_db.find_user_by_name()
        email = user_db.find_user_by_email()

        if email:
            raise RegisterException(error_code=ErrorCodes.EMAIL_ALREADY_REGISTERED, status_code=400)
        if username:
            raise RegisterException(error_code=ErrorCodes.USERNAME_ALREADY_EXISTS, status_code=400)

        hashed_password_response = await hash_password(user_data.password, None, salt="random_salt")
        hashed_password = hashed_password_response.hashed_password

        new_user_data = {
            "user_id": user_id,
            "username": user_data.username,
            "newEmail": user_data.email,
            "displayName": user_data.displayName or user_data.username,
            "hashed_password": hashed_password
        }

        user_db.insert_user(new_user_data)

