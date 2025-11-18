from Services.strategies import VOTE_STRATEGIES
from Services.vote_actions import VoteActions
from Services.strategies.session.session_status_handlers import STATUS_HANDLERS

actions = VoteActions()


async def mute(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("Reply to a user's message to start a vote.")

    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    initiator = update.effective_user

    session, status = actions.start_vote(
        chat_id=chat_id,
        target_user_id=target.id,
        initiator_user_id=initiator.id,
        is_target_bot=target.is_bot
    )

    handler = STATUS_HANDLERS.get(status)

    if handler:
        await handler(update, session)
    else:
        await update.message.reply_text("Internal error.")



async def vote_handler(update, context):
    query = update.callback_query

    session_id, vote_type = query.data.split("_")

    status = actions.cast_vote(session_id, query.from_user.id, vote_type)
    strategy = VOTE_STRATEGIES.get(status)

    if not strategy:
        return await query.edit_message_text("Internal error.")

    await strategy.execute(query, actions, session_id)
    return None
