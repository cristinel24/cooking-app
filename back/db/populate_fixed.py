import datetime
import bson
from bson import utc
from utils.init_tables import *
from utils.utils import *


@static_vars(VALID_ALLERGENS=["milk, eggs, fish, peanuts, wheat"])
def get_allergen():
    return random_from(get_allergen.VALID_ALLERGENS)


user1 = {
    "id": generate_id(counters_collection),
    "username": "username1",
    "email": "mail.fii@gmail.com",
    "icon": "my-icon.png",
    "displayName": "Karma",
    "roles": 2,
    "ratingSum": 0,
    "ratingCount": 0,
    "description": "This is my very real description!",
    "login": {
        "emailStatus": "Confirmed",
        "hashAlgName": "random_sha256",
        "hash": "password",
        "salt": "useless_salt_for_password",
        "changeToken": None,
    },
    "messageHistory": [
        "A recent message in history",
        "A more recent message in history",
        "Latest history message",
    ],
    "searchHistory": [
        "A recent search",
        "A more recent search",
        "Latest search",
    ],
    "recipes": [],
    "allergens": [],
    "ratings": [],
    "sessions": [],
    "savedRecipes": []
}
