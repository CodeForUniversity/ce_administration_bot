from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from Models.base import Base

class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint('session_id', 'voter_id', name='_session_voter_uc'),
        Index('idx_session_vote_type', 'session_id', 'vote_type'),
    )

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("vote_sessions.id"), nullable=False)
    voter_id = Column(Integer, nullable=False)
    vote_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("VoteSession", back_populates="votes")
