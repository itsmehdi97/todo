

import enum
from datetime import datetime
from typing import Optional

from schemas.base import BaseSchema


class Role(enum.Enum):
    DEV = "developer"
    MANAGER = "manager"


class UserBase(BaseSchema):
    username: str
    role: Role


class UserCreate(UserBase):
    password: str

    is_active: Optional[bool] = True


class User(UserBase):
    id: int
    is_active: Optional[bool]

    class Config:
        orm_mode = True


class UserInDb(User):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: Optional[bool]
    password: str

    class Config:
        orm_mode = True


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    sub: Optional[str]=None
    uid: Optional[int]=None
    exp: Optional[int]=None
