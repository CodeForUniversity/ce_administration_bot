from telegram import ChatPermissions

from .base import BaseStrategy

class CompletedStrategy(BaseStrategy):
    async def execute(self, query, manager, session_id):
        bot = query.message.get_bot()

        chat_id, target_id, until = manager.service.mute_user(session_id)

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=target_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until
        )
        await query.edit_message_text(f"User muted until {until}.")


