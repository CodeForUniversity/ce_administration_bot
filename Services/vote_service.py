from Utils.db import SessionLocal
from Models.vote_session import VoteSession
from Models.vote import Vote
from Models.UserPunishment import UserPunishment
from datetime import datetime, timedelta, time, timezone
import zoneinfo

VOTE_THRESHOLD = 1
SESSION_LIFETIME = timedelta(hours=24)


class VoteService:
    def __init__(self):
        self.db = SessionLocal()
        self.IRAN_TZ = zoneinfo.ZoneInfo("Asia/Tehran")

    def start_session(self, chat_id: int, target_user_id: int, initiator_user_id: int, is_target_bot: bool):
        if is_target_bot:
            return None, "target_is_bot"

        one_week_ago = datetime.utcnow() - timedelta(days=7)
        recent_session = (
            self.db.query(VoteSession)
            .filter_by(chat_id=chat_id, initiator_user_id=initiator_user_id)
            .filter(VoteSession.start_time >= one_week_ago)
            .first()
        )
        if recent_session:
            return None, "too_soon"

        existing = (
            self.db.query(VoteSession)
            .filter_by(chat_id=chat_id, target_user_id=target_user_id, status="open")
            .first()
        )
        if existing:
            return existing, "already_open"

        session = VoteSession(
            chat_id=chat_id,
            target_user_id=target_user_id,
            initiator_user_id=initiator_user_id
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session, "created"

    def cast_vote(self, session_id, voter_id, vote_type: str):
        session = self.db.query(VoteSession).filter_by(id=session_id).first()
        if not session:
            return "no_session"

        if session.status != "open":
            return "closed"

        if datetime.utcnow() - session.start_time > SESSION_LIFETIME:
            session.status = "expired"
            self.db.commit()
            return "expired"

        if self.has_already_voted(session_id, voter_id):
            return "duplicate"

        vote = Vote(session_id=session_id, voter_id=voter_id, vote_type=vote_type)
        self.db.add(vote)
        self.db.commit()

        yes, no = self.get_counts(session_id)
        if (yes - no) >= VOTE_THRESHOLD:
            session.status = "completed"
            self.db.commit()
            self.mute_user(session_id)
            return "completed"

        return "voted"

    def has_already_voted(self, session_id: int, voter_id: int) -> bool:
        return bool(
            self.db.query(Vote)
            .filter_by(session_id=session_id, voter_id=voter_id)
            .first()
        )

    def get_counts(self, session_id: int):

        yes_count = self.db.query(Vote).filter_by(session_id=session_id, vote_type="yes").count()
        no_count = self.db.query(Vote).filter_by(session_id=session_id, vote_type="no").count()
        return yes_count, no_count

    def mute_user(self, session_id: int):
        session = self.db.query(VoteSession).filter_by(id=session_id).first()
        until = self.compute_ban_until()

        punish = self.db.query(UserPunishment).filter_by(
            user_id=session.target_user_id,
            chat_id=session.chat_id
        ).first()

        if not punish:
            punish = UserPunishment(
                user_id=session.target_user_id,
                chat_id=session.chat_id,
                ban_count=1,
                is_muted=True,
                mute_until=until
            )
            self.db.add(punish)
        else:
            punish.ban_count += 1
            punish.is_muted = True
            punish.mute_until = until

        self.db.commit()

        return session.chat_id, session.target_user_id, until

    def compute_ban_until(self):

        now_ir = datetime.now(self.IRAN_TZ)
        tomorrow_date = now_ir.date() + timedelta(days=1)
        ban_ir = datetime.combine(tomorrow_date, time(3, 30), tzinfo=self.IRAN_TZ)
        return ban_ir.astimezone(timezone.utc)
