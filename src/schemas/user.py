from pydantic import BaseModel, EmailStr
from typing import Optional, List
from src.models.models import UserRole
from datetime import datetime
from pydantic import Field

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    hourly_rate: Optional[float] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None
    hourly_rate: Optional[float] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole
    hourly_rate: Optional[float] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserUpdateResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole
    hourly_rate: Optional[float] = None
    created_at: Optional[datetime] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

    class Config:
        from_attributes = True