from .base import BaseStrategy

class DuplicateStrategy(BaseStrategy):
    async def execute(self, query, manager, session_id):

        await query.answer("You have already voted.", show_alert=False)
