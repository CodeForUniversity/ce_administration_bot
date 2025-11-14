from datetime import datetime, timedelta
from Utils.db import SessionLocal
from Models.vote_session import VoteSession
from Models.vote import Vote

VOTE_THRESHOLD = 20
SESSION_LIFETIME = timedelta(hours=24)

class VoteService:
    def __init__(self):
        self.db = SessionLocal()

    def start_session(self, chat_id, target_user_id):
        existing = (
            self.db.query(VoteSession)
            .filter_by(chat_id=chat_id, target_user_id=target_user_id, status="open")
            .first()
        )

        if existing:
            return existing, False

        session = VoteSession(chat_id=chat_id, target_user_id=target_user_id)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session, True

    def cast_vote(self, session_id, voter_id):
        session = self.db.query(VoteSession).filter_by(id=session_id).first()
        if not session:
            return None, "no_session"

        if session.status != "open":
            return None, "closed"

        if datetime.utcnow() - session.start_time > SESSION_LIFETIME:
            session.status = "expired"
            self.db.commit()
            return None, "expired"

        # Check no duplication
        already = (
            self.db.query(Vote)
            .filter_by(session_id=session_id, voter_id=voter_id)
            .first()
        )

        if already:
            return session, "duplicate"

        vote = Vote(session_id=session_id, voter_id=voter_id)
        self.db.add(vote)
        self.db.commit()

        # Check threshold
        count = self.db.query(Vote).filter_by(session_id=session_id).count()
        if count >= VOTE_THRESHOLD:
            session.status = "completed"
            self.db.commit()
            return session, "completed"

        return session, "voted"
