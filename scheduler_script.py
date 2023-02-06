import time
import telebot
from weather_parser import info_dm
from datetime import datetime, timedelta

bot = telebot.TeleBot('5644371123:AAERZpN6VG5xijGF2CZUvr2DjY97w7gLxko', parse_mode=None)
BOT_URL = "URL"


while True:
    twomorrow_date = datetime.now() + timedelta(days=1)
    twomorrow_day = twomorrow_date.strftime("%d.%m.%Y")
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M")
    print(current_time)
    time.sleep(5)
    if current_time == '11:04':
        x = info_dm()
        msg = f'Прогноз на:\t\t{twomorrow_day}\n\n{x["00:00"]["time"]}{x["00:00"]["temp"]: ^10}{x["00:00"]["icon"]}\n{x["03:00"]["time"]}{x["03:00"]["temp"]: ^10}{x["03:00"]["icon"]}\n{x["06:00"]["time"]}{x["06:00"]["temp"]: ^10}{x["06:00"]["icon"]}\n{x["09:00"]["time"]}{x["09:00"]["temp"]: ^10}{x["09:00"]["icon"]}\n{x["12:00"]["time"]}{x["12:00"]["temp"]: ^10}{x["12:00"]["icon"]}\n{x["15:00"]["time"]}{x["15:00"]["temp"]: ^10}{x["15:00"]["icon"]}\n{x["18:00"]["time"]}{x["18:00"]["temp"]: ^10}{x["18:00"]["icon"]}\n{x["21:00"]["time"]}{x["21:00"]["temp"]: ^10}{x["21:00"]["icon"]}\n'
        bot.send_message(-713231502, msg)


bot.infinity_polling()