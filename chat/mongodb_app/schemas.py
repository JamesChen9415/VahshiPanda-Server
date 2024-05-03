from typing import Deque, List
from pydantic import BaseModel, Field
from .model import MessageModel


class MessageInsert(BaseModel):
    chat_channel_id: str
    msg_from: str = Field(...)
    msg_to: str = Field(...)
    content: str = Field(...)


class MessageInsertResp(BaseModel):
    chat_channel_id: str
    msg_id: str


class MessageRetrieve(BaseModel):
    chat_channel_id: str = Field(...)
    skip: int = Field(...)
    limit: int = Field(...)


class MessageRetrieveResp(MessageRetrieve):
    messages: List[MessageModel]


class MessageDelete(BaseModel):
    chat_channel_id: str = Field(...)
    msg_ids: List[str] = Field(...)
