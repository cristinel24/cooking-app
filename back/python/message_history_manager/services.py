from exceptions import MessageHistoryException
from repository import MessageHistoryCollection

message_history_collection = MessageHistoryCollection()


async def get_message_history(user_id: str, start: int, count: int) -> list[str]:
    try:
        return message_history_collection.get_message_history(user_id, start, count)
    except MessageHistoryException as e:
        raise MessageHistoryException(e.error_code, e.status_code)


async def add_message_history(user_id: str, message: str):
    try:
        message_history_collection.add_message_history(user_id, message)
    except MessageHistoryException as e:
        raise MessageHistoryException(e.error_code, e.status_code)


async def clear_message_history(user_id: str):
    try:
        message_history_collection.clear_message_history(user_id)
    except MessageHistoryException as e:
        raise MessageHistoryException(e.error_code, e.status_code)
