from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base

class VoteSession(Base):
    __tablename__ = "vote_sessions"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    target_user_id = Column(Integer, nullable=False)
    status = Column(String, default="open")  # open, expired, completed
    start_time = Column(DateTime, default=datetime.utcnow)
    votes = relationship("Vote", back_populates="session")
