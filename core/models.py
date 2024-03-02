from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean, MetaData, Table, JSON
from datetime import datetime
from sqlalchemy import UUID
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uuid

metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False),
    Column("permissions", JSON)
)
users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"))

)
chat_types = Table(
    "chat_types",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('prompt', JSON, nullable=False),
)

chats = Table(
    "chats",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('chat_type_id', UUID(as_uuid=True), ForeignKey("chat_types.id")),
    Column('history', JSON, nullable=False)


)
messages = Table(
    "message",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('chat_id', UUID(as_uuid=True), ForeignKey("chats.id")),
    Column('body', JSON, nullable=False)
)








class UserCreate(BaseModel):

    username: str
    email: str
    hashed_password: str
    is_active: bool = True

class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    content: str

class Message(MessageCreate):
    id: int
    timestamp: datetime
    user_id: int

    owner: User
    statuses: List["MessageStatus"]

    class Config:
        orm_mode = True

class AudioMessageCreate(BaseModel):
    audio_url: str
    duration: int

class AudioMessage(AudioMessageCreate):
    id: int
    user_id: int

    owner: User

    class Config:
        orm_mode = True

class ChatGroupCreate(BaseModel):
    name: str
    description: str

class ChatGroup(ChatGroupCreate):
    id: int
    members: List["GroupMember"]

    class Config:
        orm_mode = True

class GroupMemberCreate(BaseModel):
    user_id: int
    group_id: int
    is_admin: bool = False

class GroupMember(GroupMemberCreate):
    id: int
    user: User
    group: ChatGroup

    class Config:
        orm_mode = True

class MessageStatusCreate(BaseModel):
    status: str

class MessageStatus(MessageStatusCreate):
    id: int
    message_id: int
    updated_at: datetime

    message: Message

    class Config:
        orm_mode = True