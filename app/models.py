from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    rating = Column(Float, nullable=True, index=True)
    category = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
