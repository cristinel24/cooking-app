import datetime
from utils.init_tables import *
from utils.utils import *

VALID_INGREDIENTS = ["milk", "eggs", "fish", "peanuts", "flour"]


@static_vars(VALID_ALLERGENS=["milk", "eggs", "fish", "peanuts", "flour"], counter=[0, 0, 0, 0, 0])
def get_allergen(index: int) -> tuple[str, int]:
    get_allergen.counter[index] += 1
    return get_allergen.VALID_ALLERGENS[index], get_allergen.counter[index]


user1 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "username": "username1",
    "email": "mail.fii1@gmail.com",
    "icon": "my-icon.png",
    "displayName": "Karma",
    "roles": 2,
    "ratingSum": 7,
    "ratingCount": 2,
    "description": "This is my very real description!",
    "login": {
        "emailStatus": "Confirmed",
        "hashAlgName": "random_sha256",
        "hash": "passwordpassword",
        "salt": "useless_salt_for_password",
        "newEmail": None,
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
    "allergens": [get_allergen(0)[0], get_allergen(1)[0], get_allergen(2)[0]],
    "ratings": [],
    "savedRecipes": []
}
token1 = {
    "createdAt": datetime.datetime.now(datetime.timezone.utc),
    "userId": user1["id"],
    "value": "tokentokentokentoken1",
    "tokenType": "session"
}
token2 = {
    "createdAt": datetime.datetime.now(datetime.timezone.utc),
    "userId": user1["id"],
    "value": "tokentokentokentoken2",
    "tokenType": "session"
}
user2 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "username": "username2",
    "email": "mail.fii2@gmail.com",
    "icon": "my-icon2.png",
    "displayName": "Yorknez",
    "roles": 6,
    "ratingSum": 0,
    "ratingCount": 0,
    "description": "This is my very real description!",
    "login": {
        "emailStatus": "Confirmed",
        "hashAlgName": "random_sha256",
        "hash": "passwordpassword",
        "salt": "useless_salt_for_password",
        "newEmail": None,
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
    "allergens": [get_allergen(0)[0], get_allergen(1)[0], get_allergen(2)[0], get_allergen(3)[0],
                  get_allergen(4)[0]],
    "ratings": [],
    "savedRecipes": []
}
user3 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "username": "username3",
    "email": "mail.fii3@gmail.com",
    "icon": "my-icon3.png",
    "displayName": "cristinel",
    "roles": 2,
    "ratingSum": 0,
    "ratingCount": 0,
    "description": "This is my very real description!",
    "login": {
        "emailStatus": "Confirmed",
        "hashAlgName": "random_sha256",
        "hash": "passwordpassword",
        "salt": "useless_salt_for_password",
        "newEmail": None,
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
    "allergens": [get_allergen(0)[0], get_allergen(4)[0]],
    "ratings": [],
    "savedRecipes": []
}
token4 = {
    "createdAt": datetime.datetime.now(datetime.timezone.utc),
    "userId": user3["id"],
    "value": "tokentokentokentoken4",
    "tokenType": "usernameChange"
}

user4 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "username": "username4",
    "email": None,
    "icon": "my-icon4.png",
    "displayName": "razvan",
    "roles": 2,
    "ratingSum": 0,
    "ratingCount": 0,
    "description": "This is my very real description!",
    "login": {
        "emailStatus": "Pending",
        "hashAlgName": "random_sha256",
        "hash": "passwordpassword",
        "salt": "useless_salt_for_password",
        "newEmail": "mail.fii4@gmail.com",
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
    "allergens": [get_allergen(0)[0], get_allergen(4)[0]],
    "ratings": [],
    "savedRecipes": []
}
token3 = {
    "createdAt": datetime.datetime.now(datetime.timezone.utc),
    "userId": user4["id"],
    "value": "tokentokentokentoken",
    "tokenType": "emailConfirm"
}

recipe1 = {
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "id": generate_id(counters_collection),
    "authorId": user1["id"],
    "title": "Vegetarian lasagne",
    "description": "Make our easy vegetable lasagne using just a few ingredients. You can use ready-made tomato sauce "
                   "and white sauce, or batch cook the sauces and freeze them",
    "prepTime": 95,
    "steps": [
        "To make the tomato sauce, heat the olive oil in a saucepan. Add the onions, garlic and carrot. Cook for 5-7 "
        "mins over a medium heat until softened. Turn up the heat a little and stir in the tomato purée. Cook for 1 "
        "min, pour in the white wine, then cook for 5 mins until this has reduced by two-thirds. Pour over the "
        "chopped tomatoes and add the basil leaves. Bring to the boil then simmer for 20 mins. Leave to cool then "
        "whizz in a food processor. Will keep, cooled, in the fridge for up to three days or frozen for three months.",

        "To make the white sauce, melt the butter in a saucepan, stir in the plain flour, then cook for 2 mins. "
        "Slowly whisk in the milk, then bring to the boil, stirring. Turn down the heat, then cook until the sauce "
        "starts to thicken and coats the back of a wooden spoon. Will keep, cooled, in the fridge for up to three "
        "days or frozen for three months.",

        "Heat the oven to 200C/180C fan/gas 6. Lightly oil two large baking trays and add the peppers and aubergines. "
        "Toss with the olive oil, season well, then roast for 25 mins until lightly browned.",

        "Reduce the oven to 180C/160C fan/gas 4. Lightly oil a 30 x 20cm ovenproof dish. Arrange a layer of the "
        "vegetables on the bottom, then pour over a third of the tomato sauce. Top with a layer of lasagne sheets, "
        "then drizzle over a quarter of the white sauce. Repeat until you have three layers of pasta.",

        "Spoon the remaining white sauce over the pasta, making sure the whole surface is covered, then scatter over "
        "the mozzarella and cherry tomatoes. Bake for 45 mins until bubbling and golden.",
    ],
    "ingredients": [
        "3 red peppers, cut into large chunks",
        "2 aubergines, cut into ½ cm thick slices",
        "8 tbsp olive oil, plus extra for the dish",
        "300g lasagne sheets",
        "125g mozzarella",
        "handful cherry tomatoes, halved",
        "1 tbsp olive oil",
        "2 onions, finely chopped",
        "2 garlic cloves, sliced",
        "1 carrot, roughly chopped",
        "2 tbsp tomato purée",
        "200ml white wine",
        "3 x 400g cans chopped tomatoes",
        "1 bunch of basil, leaves picked",
        "85g butter",
        "85g plain flour",
        "750ml milk",
    ],
    "allergens": [
        "flour",
        "milk"
    ],
    "tags": [
        "Vegetarian",
        "Lasagne",
    ],
    "tokens": [

    ],
    "ratings": [

    ],
    "thumbnail": "default-img.png",
    "viewCount": 10,
    "ratingCount": 2,
    "ratingSum": 7,
}

rating1 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "authorId": user2["id"],
    "parentType": "recipe",
    "parentId": recipe1["id"],
    "rating": 5,
    "description": "Great!!! So delicious!!!!!!",
    "children": [],
}
rating2 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "authorId": user3["id"],
    "parentType": "recipe",
    "parentId": recipe1["id"],
    "rating": 2,
    "description": "Cool but I'm allergic 😢",
    "children": [],
}
rating3 = {
    "id": generate_id(counters_collection),
    "updatedAt": datetime.datetime.now(datetime.timezone.utc),
    "authorId": user1["id"],
    "parentType": "rating",
    "parentId": rating1["id"],
    "rating": 0,
    "description": "Thank you!",
    "children": [],
}
rating1["children"].append(rating3["id"])
user1["ratings"].append(rating3["id"])
user2["ratings"].append(rating1["id"])
user3["ratings"].append(rating2["id"])
user2["savedRecipes"].append(recipe1["id"])

allergen_collection.insert_many(
    [
        {
            "allergen": get_allergen(i)[0],
            "counter": get_allergen(i)[1]
        }
        for i in range(0, 5)
    ]
)

report1 = {
    "id": generate_id(counters_collection),
    "authorId": user1["id"],
    "reportedId": rating2["id"],
    "content": "Why am I getting a bad rating because the user is allergic?!?!",
    "reportedType": "rating",
}

report_collection.insert_one(report1)
user_collection.insert_many([user1, user2, user3])
recipe_collection.insert_one(recipe1)
rating_collection.insert_many([rating1, rating2, rating3])
tag_collection.insert_many(
    [
        {
            "tag": tag,
            "counter": 1,
        }
        for tag in recipe1["tags"]
    ]
)
follow_collection.insert_many([
    {"userId": user2["id"], "followsId": user1["id"]},
    {"userId": user3["id"], "followsId": user2["id"]},
    {"userId": user2["id"], "followsId": user3["id"]},
])
expiring_token_collection.insert_many([
    token1, token2, token3, token4
])
