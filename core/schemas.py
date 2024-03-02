from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from models import User

class TTSRequest(BaseModel):
    id: int
    pass


class TTSResponse(BaseModel):
    id: int
    pass


class STTRequest(BaseModel):
    id: int
    pass


class STTResponse(BaseModel):
    id: int
    pass


class UserCreate(BaseModel):
    id: int
    password: str
    email: str
    pass


class UserRead(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user: User
    id: int
    pass


class MessageCreate(BaseModel):
    id: int
    pass


class MessageRead(BaseModel):
    id: int
    pass


class Token(BaseModel):
    id: int
    access_token: str
    token_type: str
    pass
