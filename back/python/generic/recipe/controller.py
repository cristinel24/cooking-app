from fastapi import APIRouter
from fastapi import Request
import schemas
from bson import json_util
import services
import json

router = APIRouter(
    prefix="/api"
)

@router.get("/")
async def open():
   return "Hello world"

@router.get("/get_recipe/{recipe_name}")
async def get_recipe(recipe_name: str):
    print(recipe_name)
    return json.loads(json_util.dumps(services.get_recipe(recipe_name)))


@router.post("/create_recipe")
async def create_recipe(data: dict):
    return services.create_recipe(data)


@router.patch("/edit_recipe/{recipe_name}")
async def update_recipe(recipe_name, req:Request):
    body=await req.json()
    services.update_recipe(recipe_name,body)


@router.delete("/delete_recipe/{name}")
async def delete_recipe(name: str):
    return {services.delete_recipe(name)}


@router.get("/recipe_ratings/{parent_name}")
async def get_recipe_ratings(data: schemas.GetRatingsData):
    return {}


@router.get("/rating_replies/{parent_name}")
async def get_rating_replies(data: schemas.GetRatingsData):
    return {}


@router.post("/add_rating")
async def add_rating(data: schemas.RatingData):
    return {}


@router.patch("/edit_rating/{rating_name}")
async def edit_rating(data: schemas.EditRatingData):
    return {}


@router.delete("/delete_rating/{rating_name}")
async def delete_rating(rating_name: str):
    return {}