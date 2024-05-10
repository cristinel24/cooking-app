from pprint import pprint


def calculate_avg_rating(user_data: dict) -> int:
    pprint(user_data)
    return round(user_data["ratingSum"] / user_data["ratingCount"], 2) if user_data["ratingCount"] != 0 else 0
