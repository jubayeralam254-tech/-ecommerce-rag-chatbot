from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, nullable=False)
    business_name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    rating = Column(String)
    city = Column(String, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())