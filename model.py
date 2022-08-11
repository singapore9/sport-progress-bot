from pydantic import BaseModel


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    username: str


class ChatInfo(UserInfo):
    id: int
    type: str


class FromInfo(UserInfo):
    id: int
    is_bot: bool
    language_code: str


class MessageInfo(BaseModel):
    message_id: int
    chat: ChatInfo
    date: int
    text: str


class UserMessage(BaseModel):
    update_id: int
    message: MessageInfo
