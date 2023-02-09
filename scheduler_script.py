import time
import telebot
from weather_parser import info_weather
from datetime import datetime, timedelta

bot = telebot.TeleBot('5856331325:AAFNFv-o3O4G-2drabTJmZ21EWNQIU6fsxY', parse_mode=None)
BOT_URL = "URL"


while True:
    twomorrow_date = datetime.now() + timedelta(days=1)
    twomorrow_day = twomorrow_date.strftime("%d.%m.%Y")
    weather_dict = info_weather()
    if weather_dict == None:
        continue
    else:
        for x in weather_dict:
            msg = f'Прогноз на: {twomorrow_day}\nВ городе: {x["city"]}\n\n{x["00:00"]["time"]}{x["00:00"]["temp"]: ^10}{x["00:00"]["icon"]}\n{x["03:00"]["time"]}{x["03:00"]["temp"]: ^10}{x["03:00"]["icon"]}\n{x["06:00"]["time"]}{x["06:00"]["temp"]: ^10}{x["06:00"]["icon"]}\n{x["09:00"]["time"]}{x["09:00"]["temp"]: ^10}{x["09:00"]["icon"]}\n{x["12:00"]["time"]}{x["12:00"]["temp"]: ^10}{x["12:00"]["icon"]}\n{x["15:00"]["time"]}{x["15:00"]["temp"]: ^10}{x["15:00"]["icon"]}\n{x["18:00"]["time"]}{x["18:00"]["temp"]: ^10}{x["18:00"]["icon"]}\n{x["21:00"]["time"]}{x["21:00"]["temp"]: ^10}{x["21:00"]["icon"]}\n'
            bot.send_message(x['user_id'], msg)
    time.sleep(60)


bot.infinity_polling()