import repository

allergen_collection = repository.AllergenCollection()


async def get_allergens_by_starting_string(starting_with: str) -> list[str]:
    return await allergen_collection.get_first_allergens_starting_with(starting_with.lower())


async def inc_allergen(name: str) -> None:
    await allergen_collection.inc_allergen(name.lower())


async def inc_allergens(names: list[str]) -> None:
    await allergen_collection.inc_allergens([allergen.lower() for allergen in names])


async def dec_allergen(name: str) -> None:
    await allergen_collection.dec_allergen(name.lower())


async def dec_allergens(names: list[str]) -> None:
    await allergen_collection.dec_allergens([allergen.lower() for allergen in names])
