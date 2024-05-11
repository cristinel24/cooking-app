from repository import SearchHistoryCollection
from exceptions import SearchHistoryException

search_history_collection = SearchHistoryCollection()


# todo Auth needs to be done
async def get_search_history(user_id: str, start: int, count: int) -> list[str]:
    try:
        history = search_history_collection.get_search_history(user_id, start, count)
        if not history:
            raise SearchHistoryException(error_code=404)
        return history
    except Exception as e:
        raise SearchHistoryException(error_code=20800)


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
