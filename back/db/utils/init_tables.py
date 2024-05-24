import os
import bson
import pymongo
from pymongo import MongoClient, IndexModel

print("Connecting to kitchen db...".ljust(36, '.'), end="")
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database(os.getenv("DB_NAME"))
print("Done")

print("Cleaning the tables...".ljust(36, '.'), end="")
db.drop_collection("allergen")
db.drop_collection("counters")
db.drop_collection("expiring_token")
db.drop_collection("external_provider")
db.drop_collection("follow")
db.drop_collection("hash_algorithm")
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
            "tokenType": {"$in": ["usernameChange", "emailChange", "passwordChange", "emailConfirm"]},
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
    ),
    IndexModel(
        ["userId", "tokenType"],
        name="one_change_token_per_user",
        partialFilterExpression={
            "tokenType": {"$in": ["usernameChange", "emailChange", "passwordChange", "emailConfirm"]},
        },
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
    IndexModel(["userId", "followsId"], unique=True),
])

db.create_collection("hash_algorithm")
db.command(
    "collMod",
    "hash_algorithm",
    validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "name"],
            "properties": {
                "_id": {
                    "bsonType": "objectId",
                },
                "_class": {},
                "name": {
                    "bsonType": "string",
                    "description": "must be the name of the hash algorithm",
                },
                "primary": {},
            },
            "additionalProperties": False,
        },
    }
)
hash_algorithm_collection = db["hash_algorithm"]
hash_algorithm_collection.create_indexes([
    IndexModel(["name"], unique=True)
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
    IndexModel(["email"], unique=True, partialFilterExpression={"email": {"$type": "string"}}),
    IndexModel(["displayName"]),
    IndexModel(["id"], unique=True)
])

print("Done")

print("Preparing the counter...".ljust(36, '.'), end="")
counter = {
    "name": "id",
    "value": bson.Int64(1),
}
counter["_id"] = counters_collection.insert_one(
    counter
).inserted_id


hash_algos = ["argon2", "bcrypt", "random_sha256"]
hash_algo_dicts = list()
for hash_algo in hash_algos:
    hash_algo_dicts.append({
        "name": hash_algo
    })
    if hash_algo == "argon2":
        hash_algo_dicts[len(hash_algo_dicts) - 1]["primary"] = True

hash_algorithm_collection.insert_many(hash_algo_dicts, False)

print("Done")

