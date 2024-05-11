from repository import TokenCollection


token_db = TokenCollection()


def token_is_valid(token_value: str, token_type: str) -> dict:
    response = token_db.get_expiring_token(token_value, token_type)
    if "error_code" in response:
        return response
    return {
        "isValid": response is not None
    }


def get_token(token_value: str) -> dict:
    response = token_db.get_expiring_token(token_value)
    if "error_code" in response:
        return response
    return {
        "isValid": response is not None,
        "type": response["tokenType"] if response is not None else ''
    }

