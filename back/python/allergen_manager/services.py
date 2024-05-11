import repository

allergen_collection = repository.AllergenCollection()


async def get_allergens_by_starting_string(starting_with: str) -> list[str]:
    return allergen_collection.get_first_allergens_starting_with(starting_with.lower())


async def add_allergen_by_name(name: str) -> None:
    allergen_collection.add_allergen_by_name(name.lower())


async def remove_allergen_by_name(name: str) -> None:
    allergen_collection.remove_allergen_by_name(name.lower())
