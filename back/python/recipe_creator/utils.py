from schemas import RecipeData


def validate_recipe_data(recipe_data: RecipeData) -> bool:
    pass


def check_flags(flags: int, n: int) -> bool:
    return (flags & (1 << n)) is not 0
