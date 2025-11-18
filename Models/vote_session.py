from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base


class VoteSession(Base):
    __tablename__ = "vote_sessions"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    target_user_id = Column(Integer, nullable=False)
    initiator_user_id = Column(Integer, nullable=False)
    status = Column(String, default="open")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    votes = relationship("Vote", back_populates="session")
