import repository

tag_collection = repository.TagCollection()


async def get_tags_by_starting_string(starting_with: str) -> list[str]:
    return await tag_collection.get_first_tags_starting_with(starting_with.lower())


async def inc_tags(names: list[str]) -> None:
    await tag_collection.inc_tags([tags.lower() for tags in names])


async def dec_tags(names: list[str]) -> None:
    await tag_collection.dec_tags([tag.lower() for tag in names])
