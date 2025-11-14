from math import trunc

from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from Services.vote_service import VoteService
from Models.vote_session import VoteSession
vote_service = VoteService()

async def vote_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /vote_ban @username")

    username = context.args[0]
    chat_id = update.effective_chat.id

    try:
        user = await context.bot.get_chat(username)
    except:
        return await update.message.reply_text("User not found.")

    session, created = vote_service.start_session(chat_id, user.id)

    if not created:
        return await update.message.reply_text(
            "A vote for this user is already open."
        )

    await update.message.reply_text(
        f"Voting started for {username}. Use /yes to vote."
    )

async def vote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voter_id = update.effective_user.id
    chat_id = update.effective_chat.id
    vote_type = "yes" if update.message.text.lower() == "/yes" else "no"

    session = (
        vote_service.db.query(VoteSession)
        .filter_by(chat_id=chat_id, status="open")
        .order_by(VoteSession.start_time.desc())
        .first()
    )

    if not session:
        return await update.message.reply_text("No active voting session.")

    session, status = vote_service.cast_vote(session.id, voter_id, session.target_user_id, vote_type)

    if status == "duplicate":
        return await update.message.reply_text("You already voted.")
    if status == "expired":
        return await update.message.reply_text("The session expired.")
    if status == "voted":
        return await update.message.reply_text("Vote recorded.")
    if status == "completed":
        until = vote_service.mute_user(session.target_user_id, chat_id)
        try:
            await context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=session.target_user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until,
            )
        except Exception as e:
            return await update.message.reply_text(f"Error muting: {e}")

        return await update.message.reply_text(
            "User banned. Vote difference reached threshold."
        )
