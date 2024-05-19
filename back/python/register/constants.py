import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST_URL = os.getenv("HOST_URL", "0.0.0.0")

# URLS
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/?directConnection=true")
HASHER_API_URL = os.getenv("HASHER_API_URL", "http://0.0.0.0:8001")
HASHER_ROUTE = os.getenv("HASHER_ROUTE", "/{target}")

EMAIL_SYSTEM_API_URL = os.getenv("EMAIL_SYSTEM_API_URL", "http://0.0.0.0:8002")
EMAIL_SYSTEM_ROUTE = os.getenv("EMAIL_SYSTEM_ROUTE", "/verify-account")

TOKEN_GENERATOR_API_URL = os.getenv("TOKEN_GENERATOR_API_URL", "http://0.0.0.0:8003")
TOKEN_GENERATOR_ROUTE = os.getenv("TOKEN_GENERATOR_ROUTE", "/{user_id}/{token_type}")

TOKEN_DESTROYER_API_URL = os.getenv("TOKEN_DESTROYER_API_URL", "http://0.0.0.0:8004")
TOKEN_DESTROYER_ROUTE = os.getenv("DESTROY_TOKEN_ROUTE", "/{token}")

ID_GENERATOR_API_URL = os.getenv("ID_GENERATOR_API_URL", "http://0.0.0.0:8005")
ID_GENERATOR_ROUTE = os.getenv("ID_GENERATOR_ROUTE", "/")

USER_DESTROYER_API_URL = os.getenv("USER_DESTROYER_API_URL", "http://0.0.0.0:8006")
DESTROY_USER_ROUTE = os.getenv("DESTROY_USER_ROUTE", "/user/{user_id}")

# for database connection
MAX_TIMEOUT_SECONDS = 3


class ErrorCodes(Enum):
    EMAIL_ALREADY_REGISTERED = 25400
    USERNAME_ALREADY_EXISTS = 25401
    PASSWORD_HASHING_FAILED = 25402
    DB_CONNECTION_FAILURE = 25403
    DB_CONNECTION_TIMEOUT = 25404
    TOKEN_GENERATION_FAILED = 25405
    USER_DATA_VALIDATION_ERROR = 25406
    EMAIL_SENDING_FAILED = 25407
    DATABASE_CONNECTION_ERROR = 25408
    ID_GENERATION_FAILED = 25409
    DB_INSERTION_ERROR = 25410
