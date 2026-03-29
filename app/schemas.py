from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str
    published: bool



class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    create_at: datetime
    # owner_id: int
    owner: UserOut
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email : EmailStr
    password: str



class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None


class Vote(BaseModel):
    post_id: int
    dir: int