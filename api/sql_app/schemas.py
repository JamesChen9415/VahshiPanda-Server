from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Schemas for creating a new user.
    """

    password: SecretStr


class User(UserBase):
    """
    Schema for returning a user.
    """

    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
