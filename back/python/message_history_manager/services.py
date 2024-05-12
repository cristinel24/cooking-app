from repository import MessageHistoryCollection
from exceptions import MessageHistoryException
from constants import ErrorCodes

message_history_collection = MessageHistoryCollection()


async def get_message_history(user_id: str, start: int, count: int) -> list[str]:
    try:
        history = message_history_collection.get_message_history(user_id, start, count)
        return history
    except MessageHistoryException as e:
        raise MessageHistoryException(e.error_code, e.status_code)


async def add_message_history(user_id: str, message: str) -> bool:
    response = message_history_collection.add_message_history(user_id, message)
    if response:
        return True
    return False


async def clear_message_history(user_id: str) -> bool:
    response = message_history_collection.clear_message_history(user_id)
    if response:
        return True
    return False
