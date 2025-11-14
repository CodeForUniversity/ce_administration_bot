from telegram.ext import CommandHandler
from Handlers.vote import vote_ban, vote_handler

def setup(app):
    app.add_handler(CommandHandler("vote_ban", vote_ban))
    app.add_handler(CommandHandler("yes", vote_handler))
    app.add_handler(CommandHandler("no", vote_handler))

