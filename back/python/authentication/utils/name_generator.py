import random
from authentication.utils.base_36_convert import base_36_encode


# TODO: CHANGE TO DB COUNTER (find_one_and_update)
count = random.randint(10000000000000, 100000000000000000000)


def generate_name():
    name = base_36_encode(count)
    return name


if __name__ == "__main__":
    print(generate_name())
