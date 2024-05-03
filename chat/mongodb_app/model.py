import uuid
from typing import Deque, List, Optional, Tuple, Annotated
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


def generate_unique_id() -> str:
    return uuid.uuid4().hex


class MessageModel(BaseModel):
    msg_id: str = Field(default_factory=generate_unique_id)
    msg_from: str = Field(...)
    msg_to: str = Field(...)
    content: str = Field(...)
    create_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        schema_extra = {
            "example": {
                "msg_from": "example_from",
                "msg_to": "example_to",
                "content": "This is a test message",
                "create_at": "2023-01-01T12:00:00Z",
            }
        }


# document in mongoDB
class ChatChannelModel(BaseModel):
    chat_channel_id: str = Field(default_factory=generate_unique_id, alias="_id")
    members: List[str] = Field(...)
    messages: List[MessageModel]

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


# collection in mongoDB
class ChatCollection(BaseModel):
    """
    A container holding a list of `ChatChannelModel` instances.
    """

    chats: List[ChatChannelModel]
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
