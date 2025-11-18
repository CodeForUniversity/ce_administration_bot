from .base import BaseStrategy

class ErrorStrategy(BaseStrategy):
    async def execute(self, query, manager, session_id):
        await query.edit_message_text("Unexpected error occurred.")
