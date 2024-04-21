import random
from pprint import pprint

import pymongo
from faker import Faker
from faker_food import FoodProvider
from pymongo import MongoClient, IndexModel, errors

print("Connecting to mongodb...", end="")
client = MongoClient("mongodb://localhost:27017/?directConnection=true")
db = client["cooking_app"]
print("Done")

print("Dropping previous collections...", end="")
db.drop_collection("allergen")
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

print("Initializing collections...", end="")
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

db.create_collection("expiring_token")
db.command(
    "collMod",
    "expiring_token",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "userId", "value", "type"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "userId": {
                    "bsonType": "objectId",
                    "description": "must be the objectId of the owning user",
                },
                "value": {
                    "bsonType": "string",
                    "description": "must be a unique temporary token",
                },
                "type": {
                    "bsonType": "string",
                    "enum": ["session", "credentialChange"],
                    "description": "must be a session or credentialChange",
                },
            },
            "additionalProperties": False,
        },
    },
)

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
                "userId": {
                    "bsonType": "objectId",
                    "description": "must be the object id of an user and is required, must not be equal to followsId",
                },
                "followsId": {
                    "bsonType": "objectId",
                    "description": "must be the object id of an user and is required, must not be equal to userId",
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
                ""
            ],
            "properties": {

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
            "required": ["_id", "name", "updatedAt", "authorId", "recipeId", "rating"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "name": {
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
                    "bsonType": "objectId",
                    "description": "must be the object id of an user and is required",
                },
                "recipeId": {
                    "bsonType": "objectId",
                    "description": "must be the object id of a recipe and is required",
                },
                "rating": {
                    "bsonType": "int",
                    "minimum": 1,
                    "maximum": 5,
                    "description": "must be an integer between 1 and 5 and is required",
                },
                "description": {
                    "bsonType": "string",
                    "maxLength": 10_000,
                    "description": "must be a string of maximum 10_000 characters and is required",
                },
            },
            "additionalProperties": False,
        },
    },
)
rating_collection = db["rating"]
rating_collection.create_indexes([
    IndexModel([("authorId", pymongo.HASHED)]),
    IndexModel([("recipeId", pymongo.HASHED)]),
    IndexModel([("rating", pymongo.DESCENDING)]),
    IndexModel(["authorId", "recipeId"], unique=True),
    IndexModel(["name"], unique=True),
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
                "name",
                "updatedAt",
                "title",
                "prepTime",
                "steps",
                "ingredients",
                "allergens",
                "tags",
                "tokens",
                "ratings",
            ],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "name": {
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
                    "bsonType": "objectId",
                    "description": "must be the object id of an user",
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
                    "description": "must be an array of objectIds to ratings",
                    "items": {
                        "bsonType": ["objectId"],
                        "description": "items must be objectIds to ratings",
                    }
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
    IndexModel(
        ["authorId", "title"],
        unique=True,
        partialFilterExpression={
            "authorId": {
                "$type": "objectId"
            },
        },
    ),
    IndexModel(["name"], unique=True)
])

db.create_collection("report")
db.command(
    "collMod",
    "report",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "name", "authorId", "reportedId", "content", "type", "solved"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "name": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": 14,
                    "description": "must be a string representing the incrementor value in base 36",
                },
                "authorId": {
                    "bsonType": "objectId",
                    "description": "must be the object id of an user",
                },
                "reportedId": {
                    "bsonType": "objectId",
                    "description": "must be the object id of an user, a rating or a recipe",
                },
                "content": {
                    "bsonType": "string",
                    "minLength": 10,
                    "maxLength": 10_000,
                    "description": "must be a string of minimum 10 and maximum 10_000 characters and is required",
                },
                "type": {
                    "bsonType": "string",
                    "enum": ["user", "rating", "recipe"],
                    "description": "must be one of: user, rating or recipe",
                },
                "solved": {
                    "bsonType": "bool",
                    "description": "must be a boolean value",
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
    IndexModel([("type", pymongo.HASHED)]),
    IndexModel(["name"], unique=True)
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

db.create_collection("user")
db.command(
    "collMod",
    "user",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "_id",
                "name",
                "updatedAt",
                "username",
                "email",
                "displayName",
                "roles",
                "description",
                "savedRecipes",
                "sessions",
            ],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "name": {
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
                    "pattern": "[A-Za-z0-9_.]+",
                    "description": "must be a string",
                },
                "email": {
                    "bsonType": "string",
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
                "viewCount": {
                    "bsonType": "int",
                    "minimum": 0,
                    "description": "must be a non-negative integer"
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
                        "userChangeToken",
                        "emailConfirmToken",
                        "passwordResetToken",
                    ],
                    "properties": {
                        "emailStatus": {
                            "bsonType": "string",
                            "enum": ["Pending", "Confirmed", "Transitioning", "Banned"],
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
                        "userChangeToken": {
                            "bsonType": ["objectId", "null"],
                            "description": "must be the objectId of an expiring token",
                        },
                        "emailConfirmToken": {
                            "bsonType": ["objectId", "null"],
                            "description": "must be the objectId of an expiring token",
                        },
                        "passwordResetToken": {
                            "bsonType": ["objectId", "null"],
                            "description": "must be the objectId of an expiring token",
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
                        "bsonType": ["objectId"],
                        "description": "items must be the objectIds of recipes",
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
                "tags": {
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
                        "bsonType": ["objectId"],
                        "description": "items must be the objectIds of ratings",
                    }
                },
                "savedRecipes": {
                    "bsonType": "array",
                    "description": "must be an array containing objectIds to recipes",
                    "items": {
                        "bsonType": ["objectId"],
                        "description": "items must be the objectIds of recipes",
                    },
                },
                "sessions": {
                    "bsonType": "array",
                    "description": "must be an array containing all active user sessions",
                    "items": {
                        "bsonType": ["objectId"],
                        "description": "items must be objectIds to expiring tokens",
                    },
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
                        {"$ifNull": ["$externalLogin", False]}  # B is not null
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
    IndexModel(["name"], unique=True)
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
        "confirmed_max_chance": 0.85,
        "transitioning_max_chance": 0.90,
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


@static_vars(generated=set())
def random_base36():
    num = random.randint(1, 1_000_000_000)
    while num in random_base36.generated:
        num = random.randint(1, 1_000_000_000)

    return base36encode(num)


def random_from(arr):
    return arr[random.randint(0, len(arr) - 1)]


def random_arr(generator, range_max=params["arr"]["max"], range_min=params["arr"]["min"]):
    return [generator() for _ in range(random.randint(range_min, range_max))]


def random_unique_arr(generator, range_max=params["arr"]["max"], range_min=params["arr"]["min"]):
    return list(set([generator() for _ in range(random.randint(range_min, range_max))]))


def get_role():
    available_roles = {
        "user": 0b1,
        "verified": 0b10,
        "admin": 0b100,
        "premium": 0b1000,
    }

    role = 0

    # is premium with 20% probability
    if random.random() < params["role_premium_chance"]:
        role |= available_roles["premium"]

    role |= 1 << random.randint(0, 2)

    if role & available_roles["admin"]:
        role |= available_roles["premium"]

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
        "userId": user_id,
        "type": token_type,
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
        email_status = ["Pending", "Confirmed", "Transitioning", "Banned"]
        hash_algos = ["sha256", "sha1", "sha2", "md5", "argon2", "bcrypt"]

        status_chance = random.random()

        if status_chance < params["login_data"]["pending_max_chance"]:
            status = email_status[0]
        elif status_chance < params["login_data"]["confirmed_max_chance"]:
            status = email_status[1]
        elif status_chance < params["login_data"]["transitioning_max_chance"]:
            status = email_status[2]
        else:
            status = email_status[3]

        login_data = {
            "emailStatus": status,
            "hashAlgName": random_from(hash_algos),
            "hash": fake.sha256(),
            "salt": fake.sha256(),
            "emailConfirmToken": None,
            "passwordResetToken": None,
            "userChangeToken": None,
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
            username += ' ' + fake.user_name()

    get_user.usernames.add(username)

    email = fake.email()
    while email in get_user.emails:
        email = fake.email()

    get_user.emails.add(email)

    return {
        "updatedAt": fake.date_time(),
        "name": random_base36(),
        "username": username,
        "email": email,
        "icon": fake.url(),
        "displayName": fake.name(),
        "roles": get_role(),
        "ratingSum": 0,
        "ratingCount": 0,
        "description": fake.text(),
        field: data,
        "messageHistory": random_arr(fake.text, 10, 0),
        "searchHistory": random_arr(fake.text, 10, 0),
        "recipes": [],
        "allergens": random_unique_arr(get_allergen, 5, 0),
        "tags": random_unique_arr(get_tag, 3, 0),
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
        "updatedAt": fake.date_time(),
        "name": random_base36(),
        "authorId": None,
        "title": title,
        "ratingSum": 0,
        "ratingCount": 0,
        "description": description,
        "prepTime": random.randint(5, 10_000) // 5 * 5,
        "steps": [fake.text() for _ in range(random.randint(1, 15))],
        "ingredients": random_unique_arr(get_ingredient, 100, 1),
        "allergens": random_unique_arr(get_allergen, 20, 0),
        "tags": random_unique_arr(get_tag, 20, 0),
        "tokens": random_unique_arr(get_ingredient, 100),
        "ratings": [],
    }


def get_rating():
    return {
        "updatedAt": fake.date_time(),
        "name": random_base36(),
        "authorId": None,
        "recipeId": None,
        "rating": random.randint(1, 5),
        "description": fake.text()[:1_000],
    }


def get_report():
    report_type = ["user", "rating", "recipe"]

    return {
        "authorId": None,
        "name": random_base36(),
        "reportedId": None,
        "content": fake.text(),
        "type": random_from(report_type),
        "solved": random.random() < params["report_solved_chance"],
    }


print("Cooking up users...", end="")
# generate users
try:
    user_collection.insert_many(random_arr(get_user), False)
except errors.BulkWriteError as e:
    pprint(e.details)
    exit(0)
users = list(user_collection.find())
print("Done")

print("Cooking up recipes...", end="")
recipes = random_arr(get_recipe, 200)

# associate an author to each recipe
user_recipe_combinations = set()
for recipe in recipes:
    user = random_from(users)
    while is_unconfirmed(user) or (user['_id'], recipe['title']) in user_recipe_combinations:
        user = random_from(users)

    user_recipe_combinations.add((user["_id"], recipe['title']))
    recipe["authorId"] = user["_id"]

print("Associated authors to each recipe...", end="")

# generate recipes
try:
    recipe_collection.insert_many(recipes, False)
except errors.BulkWriteError as e:
    pprint(e.details)
    exit(0)

recipes = list(recipe_collection.find())

for user in users:
    user["savedRecipes"] = [recipe["_id"] for recipe in random.sample(recipes, k=random.randint(0, 3))]
    user_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"savedRecipes": user["savedRecipes"]}}
    )

for recipe in recipes:
    user_collection.update_one(
        {"_id": recipe["authorId"]},
        {"$push": {"recipes": recipe["_id"]}},
    )
print("Done")

print("Cooking up allergens...", end="")
# generate allergens
allergen_collection.insert_many(
    [{"allergen": k, "counter": v} for k, v in allergens.items()], False
)
print("Done")

print("Cooking up tags...", end="")
# generate tags
try:
    tag_collection.insert_many(
        [{"tag": k, "counter": v} for k, v in tags.items()], False
    )
except errors.BulkWriteError as e:
    pprint(e.details)
print("Done")

print("Cooking up external providers...", end="")
# generate external providers
external_provider_collection.insert_many(providers, False)
print("Done")

print("Cooking up follow graph...", end="")
# generate follow graph
for user in users:
    for follows in users:
        if random.random() >= params["follow_chance"]:
            continue

        if is_unconfirmed(user) or is_unconfirmed(follows):
            continue

        if user["_id"] == follows["_id"]:
            continue

        follow_collection.insert_one(
            {"userId": user["_id"], "followsId": follows["_id"]}
        )
print("Done")

print("Cooking up ratings...", end="")
# generate ratings
ratings = random_arr(get_rating, 1_000)
user_recipe_rating_combinations = set()
for rating in ratings:
    user = random_from(users)
    recipe = random_from(recipes)
    while recipe["authorId"] == user["_id"] or (user["_id"], recipe["_id"]) in user_recipe_rating_combinations:
        recipe = random_from(recipes)
        user = random_from(users)

    user_recipe_rating_combinations.add((user["_id"], recipe["_id"]))

    rating["authorId"] = user["_id"]
    rating["recipeId"] = recipe["_id"]

rating_collection.insert_many(ratings)
ratings = list(rating_collection.find())

for rating in ratings:
    user = random_from(users)
    while is_unconfirmed(user):
        user = random_from(users)

    recipe = random_from(recipes)

    user_collection.update_one(
        {"_id": rating["authorId"]},
        {
            "$inc": {"ratingSum": rating["rating"], "ratingCount": 1},
            "$push": {"ratings": rating["_id"]},
        },
    )

    recipe_collection.update_one(
        {"_id": rating["recipeId"]},
        {
            "$inc": {"ratingSum": rating["rating"], "ratingCount": 1},
            "$push": {"ratings": rating["_id"]},
        },
    )
print("Done")

print("Cooking up reports...", end="")
# generate reports
reports = random_arr(get_report)

for report in reports:
    user = random_from(users)
    while is_unconfirmed(user):
        user = random_from(users)

    report["authorId"] = user["_id"]

    if report["type"] == "user":
        reported = random_from(users)
        while is_unconfirmed(reported):
            reported = random_from(users)

        reported_id = reported["_id"]
    elif report["type"] == "rating":
        reported_id = random_from(ratings)["_id"]
    else:  # recipe
        reported_id = random_from(recipes)["_id"]

    report["reportedId"] = reported_id

report_collection.insert_many(reports)
print("Done")

print("Population script done")
