from pydantic import BaseModel, EmailStr
from typing import Optional, List
from src.models.models import UserRole

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

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True