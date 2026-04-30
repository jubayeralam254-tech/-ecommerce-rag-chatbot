from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LeadResponse(BaseModel):
    id: int
    business_name: str
    phone: str | None
    address: str | None
    rating: str | None
    city: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True