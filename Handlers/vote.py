from telegram import Update, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from Services.vote_service import VoteService
from Models.vote_session import VoteSession
from Utils.db import SessionLocal
from Utils.helper import get_vote_counts

vote_service = VoteService()

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        user = update.message.reply_to_message.from_user
    except:
        return await update.message.reply_text("User not found.")
    
    session, created = vote_service.start_session(chat_id, user.id)

    if not created:
        return await update.message.reply_text(
            "A vote for this user is already open."
        )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("YES ✅", callback_data=f"{session.id}_yes"),
            InlineKeyboardButton("NO ❌", callback_data=f"{session.id}_no")
        ]
    ])
    await update.message.reply_text(
        f"Voting started for {user.mention_html()}. Click a button to vote.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    return None

async def vote_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    voter_id = query.from_user.id
    chat_id = query.message.chat.id

    session_id, vote_type = query.data.split("_")

    session = (
        vote_service.db.query(VoteSession)
        .filter_by(chat_id=chat_id, status="open", id=session_id)
        .order_by(VoteSession.start_time.desc())
        .first()
    )

    if not session:
        return await query.edit_message_text("No active voting session.")

    session, status = vote_service.cast_vote(session.id, voter_id, session.target_user_id, vote_type)

    if status == "duplicate":
        await update_vote_message(query, session)
        return await query.answer("You already voted.", show_alert=True)

    if status == "expired":
        return await query.edit_message_text("The voting session expired.")

    if status == "voted":
        await update_vote_message(query, session)
        return await query.answer("Vote recorded.")

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
            return await query.edit_message_text(f"Error muting: {e}")

        return await query.edit_message_text(
            f"User muted til {until}."
        )
    return None


async def update_vote_message(query, session):
    yes_count, no_count = get_vote_counts(SessionLocal(), session.id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"YES ✅ ({yes_count})", callback_data=f"{session.id}_yes"),
            InlineKeyboardButton(f"NO ❌ ({no_count})", callback_data=f"{session.id}_no")
        ]
    ])

    await query.edit_message_reply_markup(reply_markup=keyboard)
