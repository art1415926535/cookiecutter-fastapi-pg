from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


PasswordField = Field(..., min_length=5, max_length=50)
EmailField = Field(..., min_length=5, max_length=100)


# Shared properties
class UserBase(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str = PasswordField


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = PasswordField


# Properties to send from API
class User(UserBase):
    id: int = Field(..., gt=0)

    class Config:
        orm_mode = True


Users = List[User]
