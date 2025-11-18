from telegram import Update
from Services.vote_actions import VoteActions

actions = VoteActions()

async def handle_target_is_bot(update: Update, session):
    await update.message.reply_text("You cannot start a vote for a bot.")

async def handle_too_soon(update: Update, session):
    await update.message.reply_text("You can only start one vote per week.")

async def handle_already_open(update: Update, session):
    await update.message.reply_text("A vote for this user is already open.")

async def handle_created(update: Update, session):
    keyboard = actions.build_keyboard(session.id)
    target = update.message.reply_to_message.from_user

    await update.message.reply_text(
        f"Voting started for {target.mention_html()}",
        parse_mode="HTML",
        reply_markup=keyboard
    )


STATUS_HANDLERS = {
    "target_is_bot": handle_target_is_bot,
    "too_soon": handle_too_soon,
    "already_open": handle_already_open,
    "created": handle_created,
}
