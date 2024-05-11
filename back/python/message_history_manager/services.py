from repository import MessageHistoryCollection

search_history_collection = MessageHistoryCollection()


# todo Auth needs to be done
async def get_message_history(user_id: str, start: int, count: int) -> list[str]:
    return search_history_collection.get_message_history(user_id, start, count)


async def add_message_history(user_id: str, message: str) -> bool:
    response = search_history_collection.add_message_history(user_id, message)
    if response:
        return True
    return False


async def clear_message_history(user_id: str) -> bool:
    response = search_history_collection.clear_message_history(user_id)
    if response:
        return True
    return False
