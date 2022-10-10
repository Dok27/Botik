from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN, APIkey
import random
import requests

open_weather_token = APIkey
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
putin = 'Путин - красавчик'
zelenskiy = 'зеленский - хуйлан'
count = 0


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
    randomizer = random.randint(1, 3)

    for text in message_array:
        def humans_win():
            file = open('humans_wins.txt', 'a')
            file.writelines('*' + '\n')
            file = open('humans_wins.txt', 'r')
            content = file.readlines()
            if ((len(content) % 10) == 2) or ((len(content) % 10) == 3) or ((len(content) % 10) == 4):
                raz = 'раза'
            else:
                raz = 'раз'
            file.close()
            return f'Человеки выйграли {len(content)} {raz}'

        def botik_win():
            file = open('botik_wins.txt', 'a')
            file.writelines('*' + '\n')
            file = open('botik_wins.txt', 'r')
            content = file.readlines()
            if ((len(content) % 10) == 2) or ((len(content) % 10) == 3) or ((len(content) % 10) == 4):
                raz = 'раза'
            else:
                raz = 'раз'
            file.close()
            return f'Ботик выйграл {len(content)} {raz}'

        if 'зеленск' in text:
            await message.reply(zelenskiy)
        elif 'путин' in text:
            await message.reply(putin)
        elif "погод" in text:
            await message.reply(get_weather("Хабаровск", open_weather_token))
            await message.reply(get_weather("Ростов-на-Дону", open_weather_token))
            await message.reply(get_weather("Кропоткин", open_weather_token))

        elif 'камень' in text:
            if randomizer == 1:
                await message.reply('Камень! \U0001f48e Ничья.')
            elif randomizer == 2:
                await message.reply('Ножницы! \u2702\uFE0F Ты выйграл!')
                await message.answer(humans_win())
            elif randomizer == 3:
                await message.reply('Хуй тебе!!! Бумага!! \U0001f4c3 Ты проиграл! Аххахахах')
                await message.answer(botik_win())

        elif 'ножницы' in text:
            if randomizer == 1:
                await message.reply('Ножницы! \u2702\uFE0F Ничья.')
            elif randomizer == 2:
                await message.reply('Бумага! \U0001f4c3 Ты выйграл!')
                await message.answer(humans_win())
            elif randomizer == 3:
                await message.reply('Хуй тебе!!! Камень!! \U0001f48e Ты проиграл! Аххахахах')
                await message.answer(botik_win())

        elif 'бумага' in text:
            if randomizer == 1:
                await message.reply('Бумага! \U0001f4c3 Ничья.')
            elif randomizer == 2:
                await message.reply('Камень! \U0001f48e Ты выйграл!')
                await message.answer(humans_win())
            elif randomizer == 3:
                await message.reply('Хуй тебе!!! Ножницы!! \u2702\uFE0F Ты проиграл! Аххахахах')
                await message.answer(botik_win())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
