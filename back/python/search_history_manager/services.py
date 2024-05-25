from repository import SearchHistoryCollection
from exceptions import SearchHistoryException

search_history_collection = SearchHistoryCollection()


async def get_search_history(user_id: str, start: int, count: int) -> list[str]:
    try:
        return search_history_collection.get_search_history(user_id, start, count)
    except SearchHistoryException as e:
        raise SearchHistoryException(e.error_code, e.status_code)


async def add_search_history(user_id: str, search_query: str):
    try:
        return search_history_collection.add_search_history(user_id, search_query)
    except SearchHistoryException as e:
        raise SearchHistoryException(e.error_code, e.status_code)


async def clear_search_history(user_id: str):
    try:
        return search_history_collection.clear_search_history(user_id)
    except SearchHistoryException as e:
        raise SearchHistoryException(e.error_code, e.status_code)
