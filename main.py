import asyncio
from fastapi import FastAPI
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import fetch_logs, router

storage = MemoryStorage()

load_dotenv()
TOKEN=os.getenv('TOKEN')
WEBHOOK_URL=os.getenv('WEBHOOK_URL')
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)
dp.include_router(router)

WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_LINK = WEBHOOK_URL + WEBHOOK_PATH

app = FastAPI()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# @app.on_event("startup")
# async def startup_event():
#     await bot.set_webhook(url=WEBHOOK_LINK)
#     print('Bot started')

# @app.post(WEBHOOK_PATH)
# async def bot_webhook(update: dict):
#     telegram_update = types.Update(**update)
#     await dp.feed_update(bot=bot, update=telegram_update)

# @app.on_event("shutdown")
# async def shutdown_event():
#     await bot.delete_webhook(drop_pending_updates=True)
#     await bot.get_session().close()
#     print('Bot stopped')

# @app.get("/")
# async def root():
#     return "Everything ok!"

# @app.get("/logs")
# async def get_logs():
#     logs = await fetch_logs()
#     return logs

