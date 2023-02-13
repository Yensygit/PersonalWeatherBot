import time
import telebot
from weather_parser import info_weather
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('6135697473:AAHn-PggauStwBHLdmulbnqXc6MhWxHWzwo', parse_mode=None)


while True:
    time.sleep(60)
    weather_dict = info_weather()
    if weather_dict == None:
        continue
    else:
        for x in weather_dict:
            msg = f"Прогноз на *{x['day']}*, *{x['city']}*\n\n{x['condition']}\nТемпература воздуха от *{x['t_min']}* до *{x['t_max']}*\nСредняя влажность воздуха: *{x['humidity_average']}*\nСкорость ветра до *{x['wind_max']}* м/с"
            bot.send_message(x['user_id'], msg, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.infinity_polling()