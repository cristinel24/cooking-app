from authentication import schemas
from authentication.utils.name_generator import generate_name
from authentication.utils.token_generator import generate_token

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
        "icon": None,
        "displayName": data.display_name,
        "roles": user_role,
        "ratingSum": 0,
        "ratingCount": 0,
        "login": {
            "emailStatus": "",
            "hashAlgName": hash.HASH_ALGORITHM,
            "hash": hash_data["hash"],
            "salt": hash_data["salt"],
            "changeToken": None,
            "newEmail": None
        },
        "externalLogin": None,


    }

    # insert in db




    # "user": 0b1,
    # "verified": 0b10, stil twitter
    # "admin": 0b100,
    # "premium": 0b1000,






def verify(token):
    pass


def login(data):
    pass


def change_username(user_name, username):
    pass


def change_email_step_1(user_name, email):
    pass


def change_email_step_2(user_name):
    pass


def change_password(user_name, password):
    pass