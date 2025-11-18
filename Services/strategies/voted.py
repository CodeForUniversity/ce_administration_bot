from .base import BaseStrategy
from .utils import update_vote_ui

class VotedStrategy(BaseStrategy):
    async def execute(self, query, manager, session_id):
        keyboard = manager.update_counts_keyboard(session_id)

        await update_vote_ui(query, keyboard=keyboard)

        await query.answer("Vote recorded ✅", show_alert=False)
