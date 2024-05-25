import pymongo.errors

from fastapi import status

from constants import Errors
from schemas import LoginData, LoginResponse
from exceptions import LoginException
from repository import UserCollection
from api import request_hash, request_token, request_user_card

user_db = UserCollection()


async def login(data: LoginData) -> dict:
    try:
        identifier = data.identifier
        password = data.password
        if "@" in identifier:
            user = user_db.find_user_by_mail(identifier)
        else:
            user = user_db.find_user_by_name(identifier)
        # If user does not exist, LoginException is raised

        # There might be externalLogin instead of login
        # since no further information was provided on how to handle it
        # im doing this
        if user["login"] is None:
            raise LoginException(Errors.INVALID_CREDS, status.HTTP_401_UNAUTHORIZED)

        user_id = user["id"]
        db_password = user["login"]["hash"]
        db_salt = user["login"]["salt"]
        db_alg_name = user["login"]["hashAlgName"]

        hasher_response = await request_hash(password, db_alg_name, db_salt)
        if hasher_response["hash"] != db_password:
            raise LoginException(Errors.INVALID_CREDS, status.HTTP_401_UNAUTHORIZED)
        token_response = await request_token(user_id, "session")
        user_card_data = await request_user_card(user_id)
        response = {
            "sessionToken": token_response.value,
            "user": user_card_data.json()
        }
        return response

    except pymongo.errors.ExecutionTimeout:
        raise LoginException(Errors.DB_TIMEOUT, status.HTTP_500_INTERNAL_SERVER_ERROR)
    except LoginException as e:
        raise e
