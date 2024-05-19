import pymongo.errors

from constants import ErrorCodes
from schemas import UserCreateData
from exceptions import RegisterException
from repository import UserCollection
from utils import match_collection_error
from api import hash_password, generate_token, generate_user_id, send_verification_email, destroy_user, destroy_token

user_db = UserCollection()


async def register(user_data: UserCreateData):
    user_id = None
    verification_token = None
    try:
        username = user_db.find_user_by_name(user_data.username)
        email = user_db.find_user_by_email(user_data.email)

        if email:
            raise RegisterException(error_code=ErrorCodes.EMAIL_ALREADY_REGISTERED, status_code=400)
        if username:
            raise RegisterException(error_code=ErrorCodes.USERNAME_ALREADY_EXISTS, status_code=400)

        user_id = await generate_user_id()

        hashed_password_response = await hash_password(user_data.password)
        hashed_password = hashed_password_response.hashed_password

        new_user_data = {
            "user_id": user_id,
            "username": user_data.username,
            "newEmail": user_data.email,
            "displayName": user_data.displayName or user_data.username,
            "login": {
                "emailStatus": "Unconfirmed",
                "hash": hashed_password,
                "salt": hashed_password_response.salt,
                "hashAlgName": hashed_password_response.hash_alg_name,
                "changeToken": None
            },
            "roles": [],
            "ratingSum": 0,
            "ratingCount": 0,
            "description": "",
            "messageHistory": [],
            "searchHistory": [],
            "recipes": [],
            "allergens": [],
            "ratings": [],
            "sessions": [],
            "savedRecipes": []
        }

        verification_token = await generate_token(user_id, "verifyAccount")
        await send_verification_email(user_data.email, verification_token)

        user_db.insert_user(new_user_data)

    except pymongo.errors.PyMongoError as e:
        if 'user_id' in locals():
            await destroy_user(user_id)
        if 'verification_token' in locals():
            await destroy_token(verification_token)

        raise match_collection_error(e)
    except RegisterException:
        if 'user_id' in locals():
            await destroy_user(user_id)
        if 'verification_token' in locals():
            await destroy_token(verification_token)

        raise RegisterException(error_code=ErrorCodes.DB_INSERTION_ERROR, status_code=500)
