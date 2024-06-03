from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Response Model for client


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # orm_mode is deprecated, Needed in case the data is not in dictionary format. Allows you to read any kind of data
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    post: Post
    votes: int

    # orm_mode is deprecated
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response model for making a user


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str = None


class Vote(BaseModel):
    post_id: int
    # dir: conint(ge=0, le=1)
    dir: Literal[0, 1]