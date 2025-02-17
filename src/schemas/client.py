from pydantic import BaseModel, EmailStr
from typing import Optional, List

class ClientBase(BaseModel):
    name: str
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    
    class Config:
        orm_mode = True