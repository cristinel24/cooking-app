from bson import ObjectId

from authentication import schemas
from authentication.utils.name_generator import generate_name
from authentication.utils.token_generator import generate_token
from db.user_collection import UserCollection
from db.expiring_token_collection import ExpiringTokenCollection

from authentication.hash import hash

from datetime import datetime


def register(data: schemas.RegisterData):
    user_role = 0b1

    password = data.password
    hash_data = hash.hash_password(password)

    user = {
        "name": generate_name(),
        "username": data.username,
        "email": data.email,
        "updatedAt": datetime.utcnow(),
        "icon": "myrealicon.png",
        "displayName": data.display_name,
        "roles": user_role,
        "ratingSum": 0,
        "ratingCount": 0,
        "description": "imi place sa mananc",
        "savedRecipes": [],
        "sessions": [],
        "login": {
            "emailStatus": "Pending",
            "hashAlgName": hash.HASH_ALGORITHM,
            "hash": hash_data["hash"],
            "salt": hash_data["salt"],
            "changeToken": None,
            "newEmail": None
        }
    }

    user_db = UserCollection()
    expiring_token_db = ExpiringTokenCollection()
    token = generate_token()

    # TODO: more robust error handling
    if user_db.get_user_by_username(user["username"]) is not None:
        return {"error": "username already exists"}
    if user_db.get_user_by_mail(user["email"]) is not None:
        return {"error": "email already exists"}


    try:
        id_user = user_db.insert_user(user)
    except Exception as e:
        return {"error:" "invalid credentials"}
    expiring_token_db.insert_token(token, ObjectId(id_user), "emailConfirm")
    return {'token': token}
    # "user": 0b1,
    # "verified": 0b10, stil twitter
    # "admin": 0b100,
    # "premium": 0b1000


def verify(token):
    expiring_token_db = ExpiringTokenCollection()
    expiring_token = expiring_token_db.get_expiring_token(token)
    if expiring_token is None:
        return {"error": "invalid token"}
    token_type = expiring_token["type"]
    if token_type == "emailConfirm":
        user_db = UserCollection()
        user = user_db.get_user_by_id(expiring_token["userId"])
        user["login"]["emailStatus"] = "Confirmed"
        user_db.update_user(user)
        return {"message": "email confirmed"}


def login(data: schemas.LoginData):
    user_db = UserCollection()
    user_id = user_db.get_user_by_username(data.identifier)
    if user_id is None:
        return {"error": "invalid username"}
    user = user_db.get_user_by_id(user_id)
    if user["login"]["emailStatus"] != "Confirmed":
        return {"error": "email not confirmed"}
    hashed_pass = hash.hash_password_with_salt(data.password, user["login"]["salt"])
    if hashed_pass != user["login"]["hash"]:
        return {"error": "invalid password"}
    token = generate_token()
    expiring_token_db = ExpiringTokenCollection()
    inserted_token_id = expiring_token_db.insert_token(token, user["_id"], "session")
    user["sessions"].append({
        "value": token,
        "type": "session",
        "_id": ObjectId(inserted_token_id)
    })
    user_db.update_user(user)
    return {"token": token}


def change_username(user_name, username):
    pass


def change_email_step_1(user_name, email):
    pass


def change_email_step_2(user_name):
    pass


def change_password(user_name, password):
    pass
