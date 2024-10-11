import os
import aiohttp
from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from dotenv import load_dotenv


load_dotenv()
OPENWEATHER_API = os.getenv("OPENWEATHER_API")
router = Router()


async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                city_name = data['name']
                temp = data['main']['temp']
                weather_description = data['weather'][0]['description']
                return f"Погода в {city_name}: {temp}°C, {weather_description}"
            else:
                return "Город не найден."


@router.message(Command(commands=['weather']))
async def send_weather(message: types.Message):
    try:
        args = message.text.split()[1]
        weather_info = await get_weather(args)
        await message.reply(weather_info)
    except IndexError:
        await message.reply("укажите город после команды. Пример: /weather Москва")
