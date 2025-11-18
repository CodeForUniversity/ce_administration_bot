from .base import BaseStrategy

class ExpiredStrategy(BaseStrategy):
    async def execute(self, query, manager, session_id):
        await query.edit_message_text("The voting session expired.")
