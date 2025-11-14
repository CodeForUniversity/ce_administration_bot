from telegram.ext import ApplicationBuilder
from dispatcher import setup
from Models.UserPunishment import UserPunishment
from Models.base import Base
from Utils.db import engine

TOKEN = "YOUR_TOKEN_HERE"

def init_db():
    Base.metadata.create_all(bind=engine)

async def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    setup(app)
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
