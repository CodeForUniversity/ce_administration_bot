from Services.vote_service import VoteService

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class VoteActions:
    def __init__(self):
        self.service = VoteService()


    def build_keyboard(self, session_id, yes=0, no=0):
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"YES ✅ ({yes})", callback_data=f"{session_id}_yes"),
                InlineKeyboardButton(f"NO ❌ ({no})", callback_data=f"{session_id}_no")
            ]
        ])

    def start_vote(self, chat_id, target_user_id):
        return self.service.start_session(chat_id, target_user_id)

    def cast_vote(self, session_id, voter_id, vote_type):
        return self.service.cast_vote(session_id, voter_id, vote_type)

    def update_counts_keyboard(self, session_id):
        yes, no = self.service.get_counts(session_id)
        return self.build_keyboard(session_id, yes, no)
