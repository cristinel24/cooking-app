import random


def base36encode(number: int):
    if not isinstance(number, int) or number < 0:
        raise TypeError("Number must be a non-negative integer")

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36 = ""

    while number:
        base36 = alphabet[number % 36] + base36
        number = number // 36

    return base36 or alphabet[0]


def generate_id(counters_collection):
    num = counters_collection.find_one_and_update(
        {"name": "id"},
        {"$inc": {"value": 1}}
    )["value"]

    return base36encode(num)


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


def random_from(arr):
    return arr[random.randint(0, len(arr) - 1)]


def random_arr(generator, range_min=0, range_max=100):
    return [generator() for _ in range(random.randint(range_min, range_max))]


def random_unique_arr(generator, range_min=0, range_max=100):
    return list(set([generator() for _ in range(random.randint(range_min, range_max))]))
