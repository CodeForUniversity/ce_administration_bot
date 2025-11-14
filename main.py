from telegram.ext import ApplicationBuilder
from dispatcher import setup
from Models.base import Base
from Utils.db import engine

TOKEN = "YOUR_TOKEN_HERE"

def init_db():
    Base.metadata.create_all(bind=engine)

def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    setup(app)
    app.run_polling()

if __name__ == "__main__":
    main()
