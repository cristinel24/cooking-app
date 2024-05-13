import json

from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))


def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def to_lower_camel_case(snake_str: str) -> str:
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]
