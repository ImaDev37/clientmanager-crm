from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str


class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    created_at: datetime

    class Config:
        from_attributes = True