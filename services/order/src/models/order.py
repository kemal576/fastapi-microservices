from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

    user = relationship("User", back_populates="orders")
