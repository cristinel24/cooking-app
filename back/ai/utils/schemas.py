from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated

import bson


def _validate_object_id(object_id):
    if not bson.ObjectId.is_valid(object_id):
        raise ValueError('Invalid ObjectId')
    return object_id


ObjectId = Annotated[str, BeforeValidator(_validate_object_id)]


class ChatbotInput(BaseModel):
    user_id: ObjectId
    user_query: str
