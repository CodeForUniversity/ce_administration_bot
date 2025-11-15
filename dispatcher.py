from telegram.ext import CommandHandler, CallbackQueryHandler
from Handlers.vote import mute, vote_handler

def setup(app):
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CallbackQueryHandler(vote_handler))
