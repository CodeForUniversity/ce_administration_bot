from sqlalchemy import func
from Models.vote import Vote

def get_vote_counts(db, session_id):
    yes = db.query(func.count(Vote.id)).filter(
        Vote.session_id == session_id,
        Vote.vote_type == "yes"
    ).scalar()

    no = db.query(func.count(Vote.id)).filter(
        Vote.session_id == session_id,
        Vote.vote_type == "no"
    ).scalar()

    return yes, no
