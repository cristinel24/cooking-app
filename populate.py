import datetime
import random

import bson
import pymongo
from bson import utc
from faker import Faker
from faker_food import FoodProvider
from pymongo import MongoClient, IndexModel

print("Connecting to kitchen db...".ljust(36, '.'), end="")
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
db = client["cooking_app"]
print("Done")

print("Cleaning the tables...".ljust(36, '.'), end="")
db.drop_collection("allergen")
db.drop_collection("counters")
db.drop_collection("expiring_token")
db.drop_collection("external_provider")
db.drop_collection("follow")
db.drop_collection("log")
db.drop_collection("rating")
db.drop_collection("recipe")
db.drop_collection("report")
db.drop_collection("tag")
db.drop_collection("user")
print("Done")

print("Initializing collections...".ljust(36, '.'), end="")
# validations
db.create_collection("allergen")
db.command(
    "collMod",
    "allergen",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "allergen", "counter"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "allergen": {
                    "bsonType": "string",
                    "minLength": 2,
                    "maxLength": 64,
                    "description": "must be a string of maximum 64 characters and is required",
                },
                "counter": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "must be a strictly positive int and is required",
                },
            },
            "additionalProperties": False,
        },
    },
)
allergen_collection = db["allergen"]
allergen_collection.create_indexes([
    IndexModel(["allergen"], unique=True),
])

db.create_collection("counters")
db.command(
    "collMod",
    "counters",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "name", "value"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "name": {
                    "bsonType": "string",
                    "description": "must be a string representing the name of the counter and is required",
                },
                "value": {
                    "bsonType": "long",
                    "description": "must be a long and is required"
                },
            },
        },
    },
)
counters_collection = db["counters"]
counters_collection.create_indexes([
    IndexModel(["name"], unique=True)
])

db.create_collection("expiring_token")
db.command(
    "collMod",
    "expiring_token",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "createdAt", "userId", "value", "tokenType"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "createdAt": {
                    "bsonType": "date",
                    "description": "must be a date representing the creation time"
                },
                "userId": {
                    "bsonType": "string",
                    "description": "must be the id of the owning user",
                },
                "value": {
                    "bsonType": "string",
                    "description": "must be a unique temporary token",
                },
                "tokenType": {
                    "bsonType": "string",
                    "enum": ["session", "usernameChange", "emailChange", "passwordChange", "emailConfirm"],
                    "description": "must be a valid type from the enum: [session, usernameChange, "
                                   "emailChange, passwordChange, emailConfirm]",
                },
            },
            "additionalProperties": False,
        },
    },
)
expiring_token_collection = db["expiring_token"]
expiring_token_collection.create_indexes([
    IndexModel(["userId", pymongo.HASHED]),
    IndexModel(
        ["createdAt"],
        name="expiring_index_credential_change",
        partialFilterExpression={
            "tokenType": "credentialChange",
        },
        expireAfterSeconds=60 * 60 * 24,
    ),
    IndexModel(
        ["createdAt"],
        name="expiring_index_session",
        partialFilterExpression={
            "tokenType": "session",
        },
        expireAfterSeconds=60 * 60 * 24 * 30,
    )
])

db.create_collection("external_provider")
db.command(
    "collMod",
    "external_provider",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "name", "endpoint"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "name": {
                    "bsonType": "string",
                    "maxLength": 64,
                    "description": "must be a string of maximum 64 characters and is required",
                },
                "endpoint": {
                    "bsonType": "string",
                    "pattern": r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9("
                               r")@:%_\+.~#?&//=]*)",
                    "maxLength": 2_048,
                    "description": "must be an url representing the endpoint of the provider and is required",
                },
            },
            "additionalProperties": False,
        },
    },
)
external_provider_collection = db["external_provider"]

db.create_collection("follow")
db.command(
    "collMod",
    "follow",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "userId", "followsId"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "userId": {
                    "bsonType": "string",
                    "description": "must be the id of an user and is required, must not be equal to followsId",
                },
                "followsId": {
                    "bsonType": "string",
                    "description": "must be the id of an user and is required, must not be equal to userId",
                },
            },
            "additionalProperties": False,
        },
        "$expr": {
            "$not": {"$eq": [
                "$userId",
                "$followsId",
            ]},
        },
    },
)
follow_collection = db["follow"]
follow_collection.create_indexes([
    IndexModel([("userId", pymongo.HASHED)]),
    IndexModel([("followsId", pymongo.HASHED)]),
])

db.create_collection("log")
db.command(
    "collMod",
    "log",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "_id",
            ],
            "properties": {
                "_id": {},
                "_class": {},
            },
            "additionalProperties": False,
        },
    },
)
log_collection = db["log"]

db.create_collection("rating")
db.command(
    "collMod",
    "rating",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "id", "updatedAt", "authorId", "rating", "parentType"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "id": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": 14,
                    "description": "must be a string representing the incrementor value in base 36",
                },
                "updatedAt": {
                    "bsonType": "date",
                    "description": "must be a date and must be modified when any other field is modified",
                },
                "authorId": {
                    "bsonType": "string",
                    "description": "must be the id of an user and is required",
                },
                "parentType": {
                    "bsonType": "string",
                    "enum": ["recipe", "rating"],
                    "description": "must be a string from the enum [\"recipe\", \"rating\"] and is required",
                },
                "parentId": {
                    "bsonType": "string",
                    "description": "must be the id of a rating or recipe and is required",
                },
                "rating": {
                    "bsonType": "int",
                    "minimum": 0,
                    "maximum": 5,
                    "description": "must be an integer between 0 and 5 and is required",
                },
                "description": {
                    "bsonType": ["string", "null"],
                    "maxLength": 10_000,
                    "description": "must be a string of maximum 10_000 characters and is required",
                },
                "children": {
                    "bsonType": ["array", "null"],
                    "description": "must be null or an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be the ids of the child comments",
                    }
                }
            },
            "additionalProperties": False,
        },
    },
)
rating_collection = db["rating"]
rating_collection.create_indexes([
    IndexModel([("authorId", pymongo.HASHED)]),
    IndexModel([("parentId", pymongo.HASHED)]),
    IndexModel([("rating", pymongo.DESCENDING)]),
    IndexModel(
        ["authorId", "parentId"],
        unique=True,
        partialFilterExpression={
            "parentType": "recipe",
        },
    ),
    IndexModel(["id"], unique=True),
])

db.create_collection("recipe")
db.command(
    "collMod",
    "recipe",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "_id",
                "id",
                "updatedAt",
                "title",
                "prepTime",
                "steps",
                "ingredients",
                "ratingSum",
                "ratingCount",
                "thumbnail",
            ],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "id": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": 14,
                    "description": "must be a string representing the incrementor value in base 36",
                },
                "updatedAt": {
                    "bsonType": "date",
                    "description": "must be a date and must be modified when any other field is modified",
                },
                "authorId": {
                    "bsonType": "string",
                    "description": "must be the id of an user",
                },
                "title": {
                    "bsonType": "string",
                    "minLength": 8,
                    "maxLength": 128,
                    "description": "must be a string of maximum 128 characters and is required",
                },
                "ratingSum": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be a non-negative integer",
                },
                "ratingCount": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be a non-negative integer",
                },
                "viewCount": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be a non-negative integer"
                },
                "description": {
                    "bsonType": "string",
                    "minLength": 80,
                    "maxLength": 10_000,
                    "description": "must be a string of maximum 10_000 characters and is required",
                },
                "prepTime": {
                    "bsonType": "int",
                    "minimum": 5,
                    "description": "must be a strictly positive integer that is a multiple of 5 and is required",
                },
                "steps": {
                    "bsonType": "array",
                    "description": "must be an array, contains at least 1 element",
                    "minItems": 1,
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "ingredients": {
                    "bsonType": "array",
                    "description": "must be an array, contains at least 1 user-assigned ingredient",
                    "minItems": 1,
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "allergens": {
                    "bsonType": "array",
                    "description": "must be an array, contains user-assigned allergens for the recipe",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "tags": {
                    "bsonType": "array",
                    "description": "must be an array, contains user-assigned tags for the recipe",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "tokens": {
                    "bsonType": ["array", "null"],
                    "description": "must be null until the tokenizing functionality is completed, after which it "
                                   "becomes an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "ratings": {
                    "bsonType": "array",
                    "description": "must be an array of ids to ratings",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be id to ratings",
                    }
                },
                "thumbnail": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                    "maxLength": 2048,
                },
            },
            "additionalProperties": False,
        },
        "$expr": {"$eq": [0, {"$mod": ["$prepTime", 5]}]},
    },
)
recipe_collection = db["recipe"]
recipe_collection.create_indexes([
    IndexModel([("title", pymongo.TEXT)]),
    IndexModel([("authorId", pymongo.HASHED)]),
    IndexModel(["tokens"]),
    IndexModel(["prepTime"]),
    IndexModel(["id"], unique=True),
    IndexModel([("viewCount", pymongo.DESCENDING)]),
])

db.create_collection("report")
db.command(
    "collMod",
    "report",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "id", "authorId", "reportedId", "content", "reportedType"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "id": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": 14,
                    "description": "must be a string representing the incrementor value in base 36",
                },
                "authorId": {
                    "bsonType": "string",
                    "description": "must be the id of an user",
                },
                "reportedId": {
                    "bsonType": "string",
                    "description": "must be the id of an user, a rating or a recipe",
                },
                "reportedType": {
                    "bsonType": "string",
                    "enum": ["user", "rating", "recipe"],
                    "description": "must be one of: [\"user\", \"rating\", \"recipe\"]",
                },
                "content": {
                    "bsonType": "string",
                    "maxLength": 10_000,
                    "description": "must be a string of minimum 10 and maximum 10_000 characters and is required",
                },
                "solver": {
                    "bsonType": "string",
                    "description": "must be the id of the solver",
                },
            },
            "additionalProperties": False,
        },
    },
)
report_collection = db["report"]
report_collection.create_indexes([
    IndexModel([("authorId", pymongo.HASHED)]),
    IndexModel([("reportedId", pymongo.HASHED)]),
    IndexModel([("reportedType", pymongo.HASHED)]),
    IndexModel(["id"], unique=True)
])

db.create_collection("tag")
db.command(
    "collMod",
    "tag",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "tag", "counter"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "tag": {
                    "bsonType": "string",
                    "maxLength": 64,
                    "description": "must be a string of maximum 64 characters and is required",
                },
                "counter": {
                    "bsonType": "int",
                    "minimum": 1,
                    "description": "must be a strictly positive int and is required",
                },
            },
            "additionalProperties": False,
        }
    },
)
tag_collection = db["tag"]
tag_collection.create_indexes([
    IndexModel(["tag"], unique=True)
])

user_change_token_embed_object = {
    "bsonType": ["object", "null"],
    "description": "must be the objectId of an expiring token",
    "additionalProperties": False,
    "required": ["_id", "value", "tokenType"],
    "properties": {
        "_id": {
            "bsonType": "objectId",
        },
        "_class": {},
        "value": {
            "bsonType": "string",
            "description": "must be the value of a valid expiring token"
        },
        "tokenType": {
            "bsonType": "string",
            "enum": [
                "session",
                "usernameChange",
                "emailChange",
                "passwordChange",
                "emailConfirm"
            ],
            "description": "must be a valid type from the enum: [session, usernameChange, "
                           "emailChange, passwordChange, emailConfirm]",
        },
    },
}

db.create_collection("user")
db.command(
    "collMod",
    "user",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "_id",
                "id",
                "updatedAt",
                "username",
                "displayName",
                "roles",
                "savedRecipes",
                "sessions",
            ],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "id": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": 14,
                    "description": "must be a string representing the incrementor value in base 36",
                },
                "updatedAt": {
                    "bsonType": "date",
                    "description": "must be a date and is required",
                },
                "username": {
                    "bsonType": "string",
                    "minLength": 8,
                    "maxLength": 64,
                    "pattern": "[A-Za-z0-9_\\.]+",
                    "description": "must be a string",
                },
                "email": {
                    "bsonType": ["string", "null"],
                    "maxLength": 256,
                    "description": "must be a string",
                },
                "icon": {
                    "bsonType": "string",
                    "maxLength": 2048,
                    "description": "must be a string of maximum 2048 characters and is required",
                },
                "displayName": {
                    "bsonType": "string",
                    "minLength": 4,
                    "maxLength": 64,
                    "description": "must be a string of maximum 64 characters and is required",
                },
                "roles": {
                    "bsonType": "int",
                    "description": "must be an integer and a valid combo of roles and is required",
                },
                "ratingSum": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be a non-negative integer",
                },
                "ratingCount": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be a non-negative integer",
                },
                "description": {
                    "bsonType": "string",
                    "maxLength": 10_000,
                    "description": "must be a string of maximum 10_000 characters and is required",
                },
                "login": {
                    "bsonType": "object",
                    "description": "must be a login data object",
                    "additionalProperties": False,
                    "required": [
                        "emailStatus",
                        "hashAlgName",
                        "hash",
                        "salt",
                    ],
                    "properties": {
                        "emailStatus": {
                            "bsonType": "string",
                            "enum": ["Pending", "Confirmed", "Transitioning"],
                        },
                        "hashAlgName": {
                            "bsonType": "string",
                            "description": "must be a string"
                        },
                        "hash": {
                            "bsonType": "string",
                            "minLength": 16,
                            "maxLength": 512,
                            "description": "must be the hash of the password using the hashAlg",
                        },
                        "salt": {
                            "bsonType": "string",
                            "minLength": 16,
                            "maxLength": 512,
                            "description": "must be the salt used in the hashing of the password",
                        },
                        "changeToken": user_change_token_embed_object,
                        "newEmail": {
                            "bsonType": ["string", "null"],
                            "description": "must "
                        }
                    },
                },
                "externalLogin": {
                    "bsonType": "object",
                    "description": "must be an external login data object",
                    "additionalProperties": False,
                    "required": [
                        "providerToken",
                        "providerData"
                    ],
                    "properties": {
                        "providerToken": {
                            "bsonType": "string",
                            "description": "must be a valid provider token",
                        },
                        "providerData": {
                            "bsonType": "string",
                            "description": "must be a valid provider",
                        },
                    },
                },
                "messageHistory": {
                    "bsonType": "array",
                    "description": "must be an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "searchHistory": {
                    "bsonType": "array",
                    "description": "must be an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "recipes": {
                    "bsonType": "array",
                    "description": "must be an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be the ids of recipes",
                    }
                },
                "allergens": {
                    "bsonType": "array",
                    "description": "must be an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be strings",
                    }
                },
                "ratings": {
                    "bsonType": "array",
                    "description": "must be an array",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be the ids of ratings",
                    }
                },
                "savedRecipes": {
                    "bsonType": "array",
                    "description": "must be an array containing ids to recipes",
                    "items": {
                        "bsonType": ["string"],
                        "description": "items must be the ids of recipes",
                    },
                },
                "sessions": {
                    "bsonType": "array",
                    "description": "must be an array containing all active user sessions",
                    "items": user_change_token_embed_object
                },
            },
            "additionalProperties": False,
        },
        "$expr": {
            "$or": [
                {
                    "$and": [
                        {"$ifNull": ["$login", False]},  # A is null
                        {"$not": {"$ifNull": ["$externalLogin", False]}},  # B is not null
                    ]
                },
                {
                    "$and": [
                        {"$not": {"$ifNull": ["$login", False]}},  # A is not null
                        {"$ifNull": ["$externalLogin", False]}  # B is null
                    ]
                }
            ]
        }
    },
)
user_collection = db["user"]
user_collection.create_indexes([
    IndexModel(["username"], unique=True),
    IndexModel(["email"], unique=True),
    IndexModel(["displayName"]),
    IndexModel(["id"], unique=True)
])

print("Done")

# generator part
fake = Faker()
fake.add_provider(FoodProvider)

allergens = {}
tags = {}
providers = [
    {"name": "Google", "endpoint": fake.url()},
    {"name": "Facebook", "endpoint": fake.url()},
    {"name": "Instagram", "endpoint": fake.url()},
]

params = {
    "arr": {
        "min": 20,
        "max": 100,
    },
    "role_premium_chance": 0.2,
    "login_data": {
        "external_chance": 0.4,
        "pending_max_chance": 0.05,
        "transitioning_max_chance": 0.10,
        "reset_state_chance": 0.3,
    },
    "report_solved_chance": 0.8,
    "follow_chance": 0.2,
}


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def base36encode(number: int):
    if not isinstance(number, int) or number < 0:
        raise TypeError("Number must be a non-negative integer")

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36 = ""

    while number:
        base36 = alphabet[number % 36] + base36
        number = number // 36

    return base36 or alphabet[0]


def generate_id():
    num = counters_collection.find_one_and_update(
        {"name": "nameIncrementor"},
        {"$inc": {"value": 1}}
    )["value"]

    return base36encode(num)


def random_from(arr):
    return arr[random.randint(0, len(arr) - 1)]


def random_arr(generator, range_min=params["arr"]["min"], range_max=params["arr"]["max"]):
    return [generator() for _ in range(random.randint(range_min, range_max))]


def random_unique_arr(generator, range_min=params["arr"]["min"], range_max=params["arr"]["max"]):
    return list(set([generator() for _ in range(random.randint(range_min, range_max))]))


available_roles = {
    "verified": 0b1,
    "admin": 0b10,
    "premium": 0b100,
    "banned": 0b1000
}


def get_role():
    role = 0

    # is premium with 20% probability
    if random.random() < params["role_premium_chance"]:
        role |= available_roles["premium"]

    if random.random() < 0.10:
        role |= available_roles["admin"]

    if role & available_roles["admin"]:
        role |= available_roles["premium"]

    if random.random() < 0.05:
        role |= available_roles["banned"]
        role &= ~available_roles["admin"]

    return role


def get_ingredient():
    ingredients = ["fruit", "ingredient", "spice", "vegetable"]

    return getattr(fake, random_from(ingredients))()


def get_allergen():
    allergen = get_ingredient()

    if allergens.get(allergen) is None:
        allergens[allergen] = 0

    allergens[allergen] += 1
    return allergen


def get_tag():
    tag = get_ingredient()

    if tags.get(tag) is None:
        tags[tag] = 0

    tags[tag] += 1
    return tag


def get_expiring_token(user_id, token_type):
    return {
        "value": fake.sha256(),
        "createdAt": datetime.datetime.now(utc),
        "userId": user_id,
        "tokenType": token_type,
    }


def get_login_data():
    login_data = None
    external_login_data = None

    # generate external login with 40% probability
    if random.random() < params["login_data"]["external_chance"]:
        external_login_data = {
            "providerToken": fake.sha256(),
            "providerData": random_from(providers)["name"],
        }
    else:
        email_status = ["Pending", "Confirmed", "Transitioning"]
        hash_algos = ["argon2", "bcrypt"]

        status_chance = random.random()

        if status_chance < params["login_data"]["pending_max_chance"]:
            user_email_status = email_status[0]
        elif status_chance < params["login_data"]["transitioning_max_chance"]:
            user_email_status = email_status[2]
        else:
            user_email_status = email_status[1]

        login_data = {
            "emailStatus": user_email_status,
            "hashAlgName": random_from(hash_algos),
            "hash": fake.sha256(),
            "salt": fake.sha256(),
            "changeToken": None,
        }

    return login_data, external_login_data


def is_unconfirmed(target_user):
    return not (
        target_user["login"]["emailStatus"] == "Confirmed"
        if target_user.get("login")
        else target_user["externalLogin"] is not None
    )


@static_vars(usernames={None}, emails={None})
def get_user():
    (login_data, external_login_data) = get_login_data()

    field = "login"
    data = login_data
    if login_data is None:
        field = "externalLogin"
        data = external_login_data

    username = None
    while username in get_user.usernames:
        username = fake.user_name()
        while len(username) < 8:
            username += '_' + fake.user_name()

    get_user.usernames.add(username)

    email = fake.email()
    while email in get_user.emails:
        email = fake.email()

    get_user.emails.add(email)

    return {
        "updatedAt": datetime.datetime.now(utc),
        "id": generate_id(),
        "username": username,
        "email": email,
        "icon": fake.url(),
        "displayName": fake.name(),
        "roles": get_role(),
        "ratingSum": 0,
        "ratingCount": 0,
        "description": fake.text(),
        field: data,
        "messageHistory": random_arr(fake.text, 0, 10),
        "searchHistory": random_arr(fake.text, 0, 10),
        "recipes": [],
        "allergens": random_unique_arr(get_allergen, 0, 5),
        "ratings": [],
        "sessions": [],
        "savedRecipes": [],
    }


def get_recipe():
    title = fake.dish()
    while len(title) < 8:
        title += ' ' + fake.dish()

    description = fake.text()
    while len(description) < 80:
        description += '\n' + fake.text()

    return {
        "updatedAt": datetime.datetime.now(utc),
        "id": generate_id(),
        "authorId": None,
        "title": title,
        "ratingSum": 0,
        "ratingCount": 0,
        "description": description,
        "prepTime": random.randint(5, 10_000) // 5 * 5,
        "steps": [fake.text() for _ in range(random.randint(1, 15))],
        "ingredients": random_unique_arr(get_ingredient, 1, 100),
        "allergens": random_unique_arr(get_allergen, 0, 20),
        "tags": random_unique_arr(get_tag, 0, 20),
        "tokens": random_unique_arr(get_ingredient, 20, 100),
        "ratings": [],
        "thumbnail": "default-img.png",
    }


def get_rating():
    return {
        "updatedAt": datetime.datetime.now(utc),
        "id": generate_id(),
        "authorId": None,
        "rating": random.randint(1, 5),
        "description": fake.text()[:1_000],
        "children": [],
    }


def get_report():
    report_type = ["user", "rating", "recipe"]

    return {
        "authorId": None,
        "id": generate_id(),
        "reportedId": None,
        "content": fake.text(),
        "reportedType": random_from(report_type),
    }


print("Preparing the counter...".ljust(36, '.'), end="")
counter = {
    "name": "nameIncrementor",
    "value": bson.Int64(1),
}
counter["_id"] = counters_collection.insert_one(
    counter
).inserted_id
print("Done")

print("Stirring up some users...".ljust(36, '.'), end="")
# generate users
users = random_arr(get_user, 150, 300)
users[0]["roles"] &= ~available_roles["banned"]
users[0]["roles"] |= available_roles["admin"]
user_collection.insert_many(users, False)
users = list(user_collection.find())
print("Done")

print("Baking fresh expiring tokens...".ljust(36, '.'), end="")
for user in users:

    no_sessions = random.randint(0, 2)
    user["sessions"] = [get_expiring_token(user["id"], "session") for _ in range(no_sessions)]
    for session in user["sessions"]:
        session["_id"] = expiring_token_collection.insert_one(
            session
        ).inserted_id

        session.pop("createdAt")
        session.pop("userId")

    user_collection.update_one(
        {"id": user["id"]},
        {"$set": {"sessions": user["sessions"]}}
    )

    if user.get("login") is None:
        continue

    status = user["login"]["emailStatus"]
    changeType = None

    if status == "Pending":
        changeType = "emailChange"
    elif status == "Confirmed":
        reset_chance = random.random()
        if reset_chance < params["login_data"]["reset_state_chance"] / 2:
            changeType = "passwordChange"
        elif reset_chance < params["login_data"]["reset_state_chance"]:
            changingField = "usernameChange"
    elif status == "Transitioning":
        changeType = "emailConfirm"

    if changeType is not None:
        expiring_token = get_expiring_token(user["id"], changeType)
        expiring_token["_id"] = expiring_token_collection.insert_one(
            expiring_token
        ).inserted_id
        expiring_token.pop("createdAt")
        expiring_token.pop("userId")

        user["login"]["changeToken"] = expiring_token
        user_collection.update_one(
            {"id": user["id"]},
            {"$set": {"login.changeToken": expiring_token}}
        )

        if status == "emailConfirm":
            user["login"]["newEmail"] = fake.email()

print("Done")

print("Cooking up recipes...".ljust(36, '.'), end="")
recipes = random_arr(get_recipe, 150, 500)

# associate an author to each recipe
for recipe in recipes:
    user = random_from(users)
    while is_unconfirmed(user):
        user = random_from(users)

    recipe["authorId"] = user["id"]

# generate recipes
recipe_collection.insert_many(recipes, False)
recipes = list(recipe_collection.find())

for user in users:
    user["savedRecipes"] = [recipe["id"] for recipe in random.sample(recipes, k=random.randint(0, 3))]
    user_collection.update_one(
        {"id": user["id"]},
        {"$set": {"savedRecipes": user["savedRecipes"]}}
    )

for recipe in recipes:
    user_collection.update_one(
        {"id": recipe["authorId"]},
        {"$push": {"recipes": recipe["id"]}},
    )
print("Done")

print("Mixing in allergens...".ljust(36, '.'), end="")
# generate allergens
allergen_collection.insert_many(
    [{"allergen": k, "counter": v} for k, v in allergens.items()], False
)
print("Done")

print("Seasoning with tags...".ljust(36, '.'), end="")
# generate tags
tag_collection.insert_many(
    [{"tag": k, "counter": v} for k, v in tags.items()], False
)
print("Done")

print("Checking up on external providers...".ljust(36, '.'), end="")
# generate external providers
external_provider_collection.insert_many(providers, False)
print("Done")

print("Brewing a flavorful follow graph...".ljust(36, '.'), end="")
# generate follow graph
for user in users:
    for follows in users:
        if random.random() >= params["follow_chance"]:
            continue

        if is_unconfirmed(user) or is_unconfirmed(follows):
            continue

        if user["id"] == follows["id"]:
            continue

        follow_collection.insert_one(
            {"userId": user["id"], "followsId": follows["id"]}
        )
print("Done")

print("Topping off with ratings...".ljust(36, '.'), end="")
# generate ratings
ratings = random_arr(get_rating, 500, 1_000)
user_recipe_rating_combinations = set()
for rating in ratings:
    user = random_from(users)
    recipe = random_from(recipes)
    while recipe["authorId"] == user["id"] or (user["id"], recipe["id"]) in user_recipe_rating_combinations:
        recipe = random_from(recipes)
        user = random_from(users)

    user_recipe_rating_combinations.add((user["id"], recipe["id"]))

    rating["authorId"] = user["id"]
    rating["parentId"] = recipe["id"]
    rating["parentType"] = "recipe"

rating_collection.insert_many(ratings)
ratings = list(rating_collection.find())

for rating in ratings:
    user = random_from(users)
    while is_unconfirmed(user):
        user = random_from(users)

    recipe = random_from(recipes)

    user_collection.update_one(
        {"id": rating["authorId"]},
        {
            "$inc": {"ratingSum": rating["rating"], "ratingCount": 1},
            "$push": {"ratings": rating["id"]},
        },
    )

    recipe_collection.update_one(
        {"id": rating["parentId"]},
        {
            "$inc": {"ratingSum": rating["rating"], "ratingCount": 1},
            "$push": {"ratings": rating["id"]},
        },
    )

replies = random_arr(get_rating, 500, 1_000)
for reply in replies:
    reply["rating"] = 0
    reply["parentType"] = "rating"

    reply["authorId"] = random_from(users)["id"]

    parent = random_from(ratings)
    reply["parentId"] = parent["id"]

    reply["_id"] = rating_collection.insert_one(
        reply
    ).inserted_id

    parent["children"].append(reply)

    rating_collection.update_one(
        {"id": parent["id"]},
        {"$push": {"children": reply["id"]}},
    )

print("Done")

print("Serving with a side of reports...".ljust(36, '.'), end="")
# generate reports
reports = random_arr(get_report, 100, 200)
admins = [user for user in users if user["roles"] & available_roles["admin"]]

for report in reports:
    user = random_from(users)
    while is_unconfirmed(user):
        user = random_from(users)

    report["authorId"] = user["id"]

    if report["reportedType"] == "user":
        reported = random_from(users)
        while is_unconfirmed(reported):
            reported = random_from(users)

        reported_id = reported["id"]
    elif report["reportedType"] == "rating":
        reported_id = random_from(ratings)["id"]
    else:  # recipe
        reported_id = random_from(recipes)["id"]

    if random.random() < params["report_solved_chance"]:
        report["solver"] = random_from(admins)["id"]

    report["reportedId"] = reported_id

report_collection.insert_many(reports)
print("Done")

print("Dish served")
