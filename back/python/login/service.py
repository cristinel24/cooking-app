import random

from constants import LoginData
from exceptions import LoginException


def login(data: LoginData) -> dict:
    random_chance = random.randint(0, 100)
    if random_chance < 50:
        raise LoginException(1, "Login failed")
    return {"test": "test"}