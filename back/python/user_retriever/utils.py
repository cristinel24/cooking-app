def calculate_avg_rating(user_data: dict) -> float:
    avg_rating = round(user_data["ratingSum"] / user_data["ratingCount"], 2) if user_data["ratingCount"] != 0 else 0
    pop_rating_sum_and_count(user_data)
    return avg_rating


def pop_rating_sum_and_count(user_data: dict) -> None:
    user_data.pop("ratingSum")
    user_data.pop("ratingCount")
