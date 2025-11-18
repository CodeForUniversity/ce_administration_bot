from .base import BaseStrategy

class NoSessionStrategy(BaseStrategy):
    async def execute(self, query, manager, session_id):
        await query.edit_message_text("No active voting session.")
