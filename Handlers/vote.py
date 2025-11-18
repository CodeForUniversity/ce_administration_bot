from Services.strategies import VOTE_STRATEGIES
from Services.vote_actions import VoteActions

actions = VoteActions()


async def mute(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to a message.")

    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user

    session, status = actions.start_vote(chat_id, target.id)

    if not status:
        return await update.message.reply_text("A vote is already open for this user.")

    keyboard = actions.build_keyboard(session.id)

    await update.message.reply_text(
        f"Voting started for {target.mention_html()}",
        parse_mode="HTML",
        reply_markup=keyboard
    )
    return None


async def vote_handler(update, context):
    query = update.callback_query

    session_id, vote_type = query.data.split("_")

    status = actions.cast_vote(session_id, query.from_user.id, vote_type)
    strategy = VOTE_STRATEGIES.get(status)

    if not strategy:
        return await query.edit_message_text("Internal error.")

    await strategy.execute(query, actions, session_id)
    return None
