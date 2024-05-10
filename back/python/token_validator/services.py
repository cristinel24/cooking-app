from repository import TokenCollection


token_db = TokenCollection()


def token_is_valid(token_value: str, token_type: str) -> dict:
    token = token_db.get_expiring_token(token_value, token_type)
    return {
        "isValid": token is not None
    }


def get_token(token_value: str) -> dict:
    token = token_db.get_expiring_token(token_value)
    return {
        "isValid": token is not None,
        "type": token["tokenType"] if token is not None else ''
    }

