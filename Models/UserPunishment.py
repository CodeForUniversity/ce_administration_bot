from sqlalchemy import Column, Integer, DateTime, Boolean
from Models.base import Base

class UserPunishment(Base):
    __tablename__ = "user_punishments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, index=True)
    chat_id = Column(Integer, nullable=False)
    ban_count = Column(Integer, default=0)
    is_muted = Column(Boolean, default=False)
    mute_until = Column(DateTime, nullable=True)
