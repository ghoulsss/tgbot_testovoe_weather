import os
import aiohttp
from aiogram import Router
from aiogram import types
from aiogram.filters import Command

from dotenv import load_dotenv

from .db import log_request


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
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                temp = data['main']['temp']
                weather_description = data['weather'][0]['description']

                return (f"Погода в {city_name}:\n"
                        f"Температура: {temp}°C\n"
                        f"Ощущается как: {feels_like}°C\n"
                        f"Описание: {weather_description}\n"
                        f"Влажность: {humidity}%\n"
                        f"Скорость ветра: {wind_speed} м/с")
            else:
                return "Город не найден."


@router.message(Command(commands=['weather']))
async def send_weather(message: types.Message):
    try:
        args = message.text.split()[1]
        weather_info = await get_weather(args)
        await log_request(message.from_user.id, message.text, weather_info)
        await message.reply(weather_info)
    except IndexError:
        await message.reply("укажите город после команды. Пример: /weather Москва")
