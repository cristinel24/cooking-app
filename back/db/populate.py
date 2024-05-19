import datetime

import bson
from bson import utc
from faker import Faker
from faker_food import FoodProvider
from utils.utils import *
from utils.init_tables import *

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

    return getattr(fake, random_from(ingredients))().lower()


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
        status_chance = random.random()

        if status_chance < params["login_data"]["pending_max_chance"]:
            user_email_status = email_status[0]
        elif status_chance < params["login_data"]["transitioning_max_chance"]:
            user_email_status = email_status[2]
        else:
            user_email_status = email_status[1]

        login_data = {
            "emailStatus": user_email_status,
            "hashAlgName": "random_sha256",
            "hash": fake.sha256(),
            "salt": fake.sha256(),
            "newEmail": None,
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
        "id": generate_id(counters_collection),
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
        "id": generate_id(counters_collection),
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
        "viewCount": random.randint(0, 100000)
    }


def get_rating():
    return {
        "updatedAt": datetime.datetime.now(utc),
        "id": generate_id(counters_collection),
        "authorId": None,
        "rating": random.randint(1, 5),
        "description": fake.text()[:1_000],
        "children": [],
    }


def get_report():
    report_type = ["user", "rating", "recipe"]

    return {
        "authorId": None,
        "id": generate_id(counters_collection),
        "reportedId": None,
        "content": fake.text(),
        "reportedType": random_from(report_type),
    }


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

        user["login"]["newEmail"] = fake.email()
        user_collection.update_one(
            {"id": user["id"]},
            {"$set": user}
        )

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

