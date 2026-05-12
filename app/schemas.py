from pydantic import BaseModel


class BusinessResponse(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    rating: float | None
    category: str
    city: str

    class Config:
        from_attributes = True


class ScrapeRequest(BaseModel):
    city: str
    category: str


class ScrapeResponse(BaseModel):
    scraped_count: int
    created_count: int
    skipped_count: int
