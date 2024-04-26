from recipe import schemas
from db import recipe_collection
from db import user_collection


def get_recipe(recipe_name: str):
    pass


def add_tokens(recipe_name: str):
    pass


def create_recipe(data: schemas.RecipeData):
    pass


def update_recipe(data: schemas.RecipeData):
    pass


def delete_recipe(name: str):
    pass


def get_recipe_ratings(data: schemas.GetRatingsData):
    pass


def get_rating_replies(data: schemas.GetRatingsData):
    pass


def add_rating(data: schemas.RatingData):
    pass


def edit_rating(data: schemas.EditRatingData):
    pass


def delete_rating(rating_name: str):
    pass