import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
HOST= os.getenv("HOST", "localhost")
PORT= int(os.getenv("PORT", 8000))
DB_NAME=os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?directConnection=true")
MAX_TIMEOUT_TIME_SECONDS = 3

ALLERGEN_MANAGER_API_URL = os.getenv("ALLERGEN_MANAGER_API_URL")
if ALLERGEN_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'ALLERGEN_MANAGER_API_URL' is not set")
DEC_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/allergens/dec"
INC_ALLERGENS_ROUTE = ALLERGEN_MANAGER_API_URL + "/allergens/inc"

TAG_MANAGER_API_URL = os.getenv("TAG_MANAGER_API_URL")
if TAG_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'TAG_MANAGER_API_URLL' is not set")
DEC_TAGS_ROUTE = TAG_MANAGER_API_URL + "/tags/dec"
INC_TAGS_ROUTE = TAG_MANAGER_API_URL + "/tags/inc"

RATING_MANAGER_API_URL = os.getenv("RATING_MANAGER_API_URL")
if RATING_MANAGER_API_URL is None:
    raise ValueError("Environment variable 'RATING_MANAGER_API_URL' is not set")
DEC_RATING_ROUTE = RATING_MANAGER_API_URL + "/rating"
INC_RATING_ROUTE = RATING_MANAGER_API_URL

IMAGES_API_URL = os.getenv("IMAGES_API_URL")
if IMAGES_API_URL is None:
    raise ValueError("Environment variable 'IMAGES_API_URL' is not set")

class ErrorCodes(Enum):
    SERVER_ERROR=26300
    RECIPE_NOT_FOUND=26301
    FAILED_DESTROY_RECIPE=26302
    RECIPE_NOT_FOUND_IN_USERS=26303
    RECIPE_FAILED_TAGS=26304
    RECIPE_FAILED_ALLERGENS=26304
    RECIPE_FAILED_RATINGS=26305
    RECIPE_FAILED_AUTHOR=26306
    NOT_RESPONSIVE_API=26307
    RECIPE_FAILED_THUMBNAIL=26308
    RATING_NOT_FOUND=26309
    

