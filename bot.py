import telebot
from weather_parser import info_dm
from dbase import create_connection, execute_query, execute_read_query

import telebot
bot = telebot.TeleBot("5644371123:AAERZpN6VG5xijGF2CZUvr2DjY97w7gLxko")

def add_time(message, user_info):
	user_info.append(message.text)
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	request_insert_user_id = f"INSERT INTO subs_weather (id_user, city_weather, format, time) VALUES ('{user_info[0]}','{user_info[2]}','{user_info[3]}','{user_info[4]}');"
	insert_user_id = execute_query(connection, request_insert_user_id)
	bot.reply_to(message, "Ваша подписака добавлена в БД. Увидеть текущие подписки можно командой /my_sub_weather")

def add_format(message, user_info):
	user_info.append(message.text)
	msg = bot.reply_to(message, "Укажите время в формате чч:мм")
	bot.register_next_step_handler(msg, add_time, user_info)

def check_city(message, user_info):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_city = f"select * from cities where number='{message.text}';"
	city = execute_read_query(connection, select_city)
	user_info.append(city[0][4])
	msg = bot.reply_to(message, "Выберите формат /сегодня /завтра /3-дня")
	bot.register_next_step_handler(msg, add_format, user_info)

def add_city(message, user_info):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_city = f"select * from cities where city='{message.text}';"
	cities = execute_read_query(connection, select_city)
	if len(cities)==1:
		user_info.append(message.text)
		msg = bot.reply_to(message, "Выбери формат /сегодня /завтра /3-дня")
		bot.register_next_step_handler(msg, add_format, user_info)
	elif len(cities)>1:
		mylist = str([str(i[0]) + ", " + str(i[1]) + ", " + str(i[2]) for i in cities])
		city = 'Найдено несколько городов с такм именем, Укажите ID подходящего города из списка:\n' + mylist
		user_info.append(message.text)
		msg=bot.reply_to(message, city)
		bot.register_next_step_handler(msg, check_city, user_info)
	elif cities == None:
		bot.reply_to(message, "ОШИБКА: Такого города нет в базе данных")




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет, бот позволяет посмотреть или подписаться на погоду, выбери что ты хочешь, выбери /sub_weather или /unsubs_weather")


@bot.message_handler(commands=['sub_weather'])
def sub_weather(message):
	user_info = []
	user_info.append(message.from_user.id)
	msg = bot.reply_to(message, "Напишите свой город")
	bot.register_next_step_handler(msg, add_city, user_info)

bot.infinity_polling()


