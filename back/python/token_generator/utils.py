import secrets


def base_36_encode(number, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    base36 = ''
    sign = ''
    if number < 0:
        sign = '-'
        number = -number
    if 0 <= number < len(alphabet):
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36
    return sign + base36


def generate_token() -> str:
    byte_token = secrets.token_bytes(32)
    int_token = int.from_bytes(byte_token, "big")
    return base_36_encode(int_token)