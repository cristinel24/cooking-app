UserCardData = {
    "username": str,
    "displayName": str,
    "icon": str,
    "roles": list[str],
    "ratingAvg": float
}

RecipeData = {
    "author": UserCardData,
    "title": str,
    "description": str,
    "prepTime": str,
    "steps": list[str],
    "ingredients": list[str],
    "allergens": list[str],
    "tags": list[str],
    "thumbnail": str,
    "viewCount": int
}

RecipeCardData = {
    "author": UserCardData,
    "title": str,
    "description": str,
    "prepTime": str,
    "tags": list[str],
    "allergens": list[str],
    "thumbnail": str,
    "viewCount": int
}