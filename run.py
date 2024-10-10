import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, напиши мне свой город!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # пользуемся при дебагинге, на проде выключаем 
    # так как замедляет сильно при увеличении пользователей
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
