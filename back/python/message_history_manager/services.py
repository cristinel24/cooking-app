from repository import MessageHistoryCollection
from exceptions import MessageHistoryException

search_history_collection = MessageHistoryCollection()


# todo Auth needs to be done
async def get_message_history(user_id: str, start: int, count: int) -> list[str]:
    try:
        history = search_history_collection.get_message_history(user_id, start, count)
        if not history:
            raise MessageHistoryException(error_code=404)
        return history
    except Exception as e:
        raise MessageHistoryException(error_code=20800)


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
