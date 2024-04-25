import secrets
from authentication.utils.base_36_convert import base_36_encode


def generate_token():
    byte_token = secrets.token_bytes(32)
    int_token = int.from_bytes(byte_token, "big")
    return base_36_encode(int_token)


if __name__ == "__main__":
    print(generate_token())
