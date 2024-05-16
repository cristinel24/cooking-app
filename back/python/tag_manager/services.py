import repository

tag_collection = repository.TagCollection()


async def get_tags_by_starting_string(starting_with: str) -> list[str]:
    return await tag_collection.get_first_tags_starting_with(starting_with.lower())


async def add_tag_by_name(name: str) -> None:
    await tag_collection.add_tag_by_name(name.lower())


async def remove_tag_by_name(name: str) -> None:
    await tag_collection.remove_tag_by_name(name.lower())
