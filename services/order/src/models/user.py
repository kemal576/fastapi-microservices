from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, unique=True, nullable=False)

    orders = relationship("Order", back_populates="user")
    notifications = relationship("UserNotification", back_populates="user")
