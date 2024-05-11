from pydantic import BaseModel


class SearchHistoryData(BaseModel):
    # might not be None?
    search_query: str | None = None
