from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("vote_sessions.id"))
    voter_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("VoteSession", back_populates="votes")
