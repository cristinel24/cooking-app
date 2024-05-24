def base36encode(number: int) -> str:
    if not isinstance(number, int) or number < 0:
        raise TypeError("Number must be a non-negative integer")

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36 = ""

    while number:
        base36 = alphabet[number % 36] + base36
        number = number // 36

    return base36 or alphabet[0]
