def calculate_avg_rating(user_data: dict) -> float:
    avg_rating = round(user_data["ratingSum"] / user_data["ratingCount"], 2) if user_data["ratingCount"] != 0 else 0
    user_data.pop("ratingSum")
    user_data.pop("ratingCount")
    return avg_rating
