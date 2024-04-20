from pydantic import BaseModel


class ChatbotInput(BaseModel):
    user_id: str
    user_query: str
