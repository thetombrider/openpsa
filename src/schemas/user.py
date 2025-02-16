from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CONSULTANT = "consultant"

class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    hourly_rate: Optional[float] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None
    hourly_rate: Optional[float] = None

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True