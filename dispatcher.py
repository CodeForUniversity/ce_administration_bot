from telegram.ext import CommandHandler
from Handlers.vote import vote_ban, vote_yes

def setup(app):
    app.add_handler(CommandHandler("vote_ban", vote_ban))
    app.add_handler(CommandHandler("yes", vote_yes))
