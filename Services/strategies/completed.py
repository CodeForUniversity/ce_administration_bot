from .base import BaseStrategy

class CompletedStrategy(BaseStrategy):
    async def execute(self, query, manager, until):
        await query.edit_message_text(f"User muted until {until}.")
