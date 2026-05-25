from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class Holding(Base):
    """Stock holding model - represents a user's stock position."""
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    purchase_date = Column(Date, nullable=False)
    risk_level = Column(String, nullable=False)  # High, Medium, Low
