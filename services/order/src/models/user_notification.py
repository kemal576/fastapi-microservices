from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class UserNotification(Base):
    __tablename__ = "user_notification"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message = Column(String, nullable=False)

    user = relationship("User", back_populates="notifications")
