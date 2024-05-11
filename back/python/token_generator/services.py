from repository import TokenCollection
from constants import TOKEN_TYPES, Errors
from api import user_exists
from utils import generate_token

token_db = TokenCollection()


def get_user_token(user_id: str, token_type: str) -> dict:
    if token_type not in TOKEN_TYPES:
        return {"error_code": Errors.INVALID_TYPE}
    if not user_exists(user_id):
        return {"error_code": Errors.USER_NOT_FOUND}
    try:
        value = generate_token()
        token = token_db.insert_token(value, user_id, token_type)
        return token
    # Eroare cu Mongo, returnam internal server error
    except Exception as e:
        print(e)
        raise e