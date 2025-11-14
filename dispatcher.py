from telegram.ext import CommandHandler, CallbackQueryHandler
from Handlers.vote import vote_ban, vote_handler

def setup(app):
    app.add_handler(CommandHandler("vote_ban", vote_ban))
    app.add_handler(CallbackQueryHandler(vote_handler))
