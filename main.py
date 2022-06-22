from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN, APIkey
import requests


open_weather_token = APIkey
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def main(city):
    get_weather(city, open_weather_token)


def get_weather(city, open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
    )
    data = r.json()

    city = data["name"]
    cur_weather = data["main"]["temp"]
    wind = data["wind"]["speed"]
    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = " "

    return (f"{city}\n Температура: {cur_weather} °С  {wd}\n Ветер: {wind} м/с")


@dp.message_handler()
async def echo_send(message: types.Message):
    Message = message.text.lower()
    message_array = Message.split()
    for text in message_array:
        if "погод" in text:
            await message.reply(get_weather("Хабаровск", open_weather_token))
            await message.reply(get_weather("Ростов-на-Дону", open_weather_token))
            await message.reply(get_weather("Кропоткин", open_weather_token))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

