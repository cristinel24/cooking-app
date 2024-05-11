from constants import ErrorCodes


def calculate_avg_rating(user_data: dict) -> float:
    return round(user_data["ratingSum"] / user_data["ratingCount"], 2) if user_data["ratingCount"] != 0 else 0


def pop_rating_sum_and_count(user_data: dict) -> None:
    user_data.pop("ratingSum")
    user_data.pop("ratingCount")


def verify_auth(user_roles: int) -> None:
    banned_user_role = 1000
    if user_roles == banned_user_role:
        raise Exception(ErrorCodes.UNAUTHORIZED.value)
