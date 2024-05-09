from bson import ObjectId
from datetime import datetime

from authentication import schemas
from authentication.hash import hash
from authentication.utils.name_generator import generate_name
from authentication.utils.token_generator import generate_token
from authentication.utils.enums import EmailStatus, ExpiringTokenType
from common.enums import UserRoles
from db.user_collection import UserCollection
from db.expiring_token_collection import ExpiringTokenCollection


user_db = UserCollection()
expiring_token_db = ExpiringTokenCollection()


def register(data: schemas.RegisterData):
    # TODO: more robust error handling
    password = data.password
    hash_data = hash.hash_password(password)

    # validation checks
    if "@" not in data.email:
        return {"error": "invalid email address"}

    # uniqueness checks
    if user_db.get_user_by_username(data.username) is not None:
        return {"error": "username already exists"}

    if user_db.get_user_by_mail(data.email) is not None:
        # send email along the lines of "someone is trying to register using your email address"
        return {"message": "an email has been sent to the email address for verification"}

    user = {
        "name": generate_name(),
        "username": data.username,
        "email": data.email,
        "updatedAt": datetime.utcnow(),
        "icon": "",
        "displayName": data.displayName,
        "roles": UserRoles.USER.value,
        "ratingSum": 0,
        "ratingCount": 0,
        "description": "",
        "savedRecipes": [],
        "sessions": [],
        "login": {
            "emailStatus": EmailStatus.PENDING.value,
            "hashAlgName": hash_data["hashAlgName"],
            "hash": hash_data["hash"],
            "salt": hash_data["salt"],
            "changeToken": None,
            "newEmail": None
        }
    }

    token = generate_token()

    try:
        id_user = user_db.insert_user(user)
    # TODO: error handling
    except Exception as e:
        return {"error": "invalid user data"}

    expiring_token_db.insert_token(token, ObjectId(id_user), "emailConfirm")
    return {"message": "an email has been sent to the email address for verification"}


def verify(token):
    expiring_token = expiring_token_db.get_expiring_token(token, ExpiringTokenType.EMAIL_CONFIRM.value)
    if expiring_token is None:
        return {"error": "invalid token"}
    user = user_db.get_user_by_id(expiring_token["userId"])
    user["login"]["emailStatus"] = EmailStatus.CONFIRMED.value
    user_db.update_user(user)
    expiring_token_db.remove_token(ObjectId(expiring_token["_id"]))
    return {"message": "email confirmed"}


def login(data: schemas.LoginData):
    # TODO: throw custom exceptions
    invalid_credentials_error = {
        "error": "invalid credentials"
    }

    if "@" in data.identifier:
        user = user_db.get_user_by_mail(data.identifier)
    else:
        user = user_db.get_user_by_username(data.identifier)

    if user is None:
        return invalid_credentials_error

    if user["login"]["emailStatus"] != EmailStatus.CONFIRMED.value:
        return {"error": "email not confirmed"}

    hashed_pass = hash.hash_password_with_salt(data.password, user["login"]["salt"])
    if hashed_pass != user["login"]["hash"]:
        return invalid_credentials_error

    # insert session token
    session_token_value = generate_token()
    inserted_token_id = expiring_token_db.insert_token(session_token_value, user["_id"], "session")

    user["sessions"].append({
        "value": session_token_value,
        "type": ExpiringTokenType.SESSION.value,
        "_id": ObjectId(inserted_token_id)
    })
    user_db.update_user(user)

    return {"session": session_token_value}


def change_username(user_name, username):
    pass


def change_email_step_1(user_name, email):
    pass


def change_email_step_2(user_name):
    pass


def change_password(user_name, password):
    pass


def is_authenticated(session_token) -> bool:
    # TODO: exception handling
    token = expiring_token_db.get_expiring_token(session_token, ExpiringTokenType.SESSION.value)
    if token is None:
        return False

    user = user_db.get_user_by_id(token["userId"])
    if user is None:
        return False

    return True
