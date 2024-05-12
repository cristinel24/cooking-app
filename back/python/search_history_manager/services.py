from repository import SearchHistoryCollection
from exceptions import SearchHistoryException
from constants import ErrorCodes

search_history_collection = SearchHistoryCollection()


async def get_search_history(user_id: str, start: int, count: int) -> list[str]:
    try:
        history = search_history_collection.get_search_history(user_id, start, count)
        return history if history else []
    except SearchHistoryException as e:
        raise SearchHistoryException(e.error_code, e.status_code)


async def add_search_history(user_id: str, search_query: str) -> bool:
    response = search_history_collection.add_search_history(user_id, search_query)
    if response:
        return True
    return False


async def clear_search_history(user_id: str) -> bool:
    response = search_history_collection.clear_search_history(user_id)
    if response:
        return True
    return False
