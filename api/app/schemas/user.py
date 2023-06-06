from pydantic import BaseModel, EmailStr
from typing import Optional

class UserTypeBase(BaseModel):
    user_type : str


class UserTypeCreate(UserTypeBase):
    pass


class UserTypeUpdate(BaseModel):
    user_type : Optional[str] = None


class UserTypeResponse(UserTypeBase):
    id : int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name : str
    username : str
    password : str
    email : EmailStr


class UserCreate(UserBase):
    type: int


class UserResponse(UserBase):
    user_id : int
    type : int
    user_type: UserTypeResponse

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name : Optional[str] = None
    username : Optional[str] = None
    password : Optional[str] = None
    email : Optional[EmailStr] = None

