from Utils.db import SessionLocal
from Models.vote_session import VoteSession
from Models.vote import Vote
from Models.UserPunishment import UserPunishment
from datetime import datetime, timedelta, time, timezone
import zoneinfo

VOTE_THRESHOLD = 20
VOTE_PERCENTAGE = 60
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

    def cast_vote(self, session_id, voter_id, target_id, vote_type: str):
        session = self.db.query(VoteSession).filter_by(id=session_id).first()
        if not session:
            return None, "no_session"

        if session.status != "open":
            return None, "closed"

        if datetime.utcnow() - session.start_time > SESSION_LIFETIME:
            session.status = "expired"
            self.db.commit()
            return None, "expired"

        already = (
            self.db.query(Vote)
            .filter_by(session_id=session_id, voter_id=voter_id)
            .first()
        )
        if already:
            return session, "duplicate"

        vote = Vote(session_id=session_id, voter_id=voter_id, target_id=target_id, vote_type=vote_type)
        self.db.add(vote)
        self.db.commit()

        yes_count = self.db.query(Vote).filter_by(session_id=session_id, vote_type="yes").count()
        no_count = self.db.query(Vote).filter_by(session_id=session_id, vote_type="no").count()

        if (yes_count - no_count) >= VOTE_THRESHOLD:
            session.status = "completed"
            self.db.commit()
            return session, "completed"

        return session, "voted"

    def compute_ban_until(self):
        IRAN = zoneinfo.ZoneInfo("Asia/Tehran")

        now_ir = datetime.now(IRAN)
        tomorrow_date = now_ir.date() + timedelta(days=1)

        ban_ir = datetime.combine(tomorrow_date, time(3, 30), tzinfo=IRAN)

        return ban_ir.astimezone(timezone.utc)

    def mute_user(self, target_user_id, chat_id):
        until = self.compute_ban_until()

        punish = self.db.query(UserPunishment).filter_by(user_id=target_user_id, chat_id=chat_id).first()
        if not punish:
            punish = UserPunishment(user_id=target_user_id, chat_id=chat_id, ban_count=1, is_muted=True, mute_until=until)
            self.db.add(punish)
        else:
            punish.ban_count += 1
            punish.is_muted = True
            punish.mute_until = until
        self.db.commit()

        return until
