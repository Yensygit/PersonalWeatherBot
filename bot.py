from telebot import types
from weather_parser import info_dm
from dbase import create_connection, execute_query, execute_read_query
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import re

import telebot
bot = telebot.TeleBot("5644371123:AAERZpN6VG5xijGF2CZUvr2DjY97w7gLxko")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, бот позволяет посмотреть или подписаться на погоду, выбери что ты хочешь, выбери /sub_weather или /unsubs_weather")


@bot.message_handler(commands=['sub_weather'])
def sub_weather(message):
	user_info = []
	quantity_try = 0
	user_info.append(message.from_user.id)
	msg = bot.send_message(message.chat.id, "Напишите свой город")
	bot.register_next_step_handler(msg, add_city, user_info, quantity_try)


def add_city(message, user_info, quantity_try):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_city = f"select * from cities where city='{str(message.text).title()}';"
	city = execute_read_query(connection, select_city)
	if len(city)==1:
		user_info.append(city[0][1])
		user_info.append(city[0][4])
		button1 = KeyboardButton('На сегодня')
		button2 = KeyboardButton('На завтра')
		button3 = KeyboardButton('На 3 дня')
		keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(button1, button2, button3)
		msg = bot.send_message(message.chat.id, "Выбери формат. Бот может прислать погоду на сегодня, на завтра или на 3 ближайших дня", reply_markup=keyboard)
		bot.register_next_step_handler(msg, add_format, user_info, quantity_try)
	elif len(city)>1:
		mylist = str([str(i[0]) + ", " + str(i[1]) + ", " + str(i[2]) for i in city])
		city = 'Найдено несколько городов с такм именем, Укажите ID подходящего города из списка:\n' + mylist
		user_info.append(message.text)
		msg=bot.send_message(message.chat.id, city)
		bot.register_next_step_handler(msg, check_city, user_info, quantity_try)
	elif len(city) == 0:
		if quantity_try < 5:
			quantity_try+=1
			bot.send_message(message.chat.id, "ОШИБКА: Такого города нет в базе данных!")
			msg = bot.send_message(message.chat.id, "Напишите свой город")
			bot.register_next_step_handler(msg, add_city, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id, "Ты ошибся в заполнении, начни заново, выбери что ты хочешь, выбери /sub_weather или /unsubs_weather")


def check_city(message, user_info, quantity_try):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_city = f"select * from cities where number='{message.text}';"
	city = execute_read_query(connection, select_city)
	if len(city) == 1:
		user_info.append(city[0][1])
		user_info.append(city[0][4])
		button1 = KeyboardButton('На сегодня')
		button2 = KeyboardButton('На завтра')
		button3 = KeyboardButton('На 3 дня')
		keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(button1, button2, button3)
		msg = bot.send_message(message.chat.id, "Выбери формат. Бот может прислать погоду на сегодня, на завтра или на 3 ближайших дня", reply_markup=keyboard)
		bot.register_next_step_handler(msg, add_format, user_info, quantity_try)
	else:
		if quantity_try < 5:
			quantity_try += 1
			bot.send_message(message.chat.id, "ОШИБКА: Такого города нет в базе данных!")
			msg = bot.send_message(message.chat.id, "Напишите свой город")
			bot.register_next_step_handler(msg, add_city, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id, "Ты ошибся в заполнении, начни заново, выбери что ты хочешь, выбери /sub_weather или /unsubs_weather")



def add_format(message, user_info, quantity_try):
	if message.text == 'На сегодня':
		user_info.append('today')
		msg = bot.send_message(message.chat.id, "Укажите время в формате чч:мм", reply_markup=ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, add_time, user_info, quantity_try)
	elif message.text == 'На завтра':
		user_info.append('tomorrow')
		msg = bot.send_message(message.chat.id, "Укажите время в формате чч:мм", reply_markup=ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, add_time, user_info,quantity_try)
	elif message.text == 'На 3 дня':
		user_info.append('3days')
		msg = bot.send_message(message.chat.id, "Укажите время в формате чч:мм", reply_markup=ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, add_time, user_info, quantity_try)
	else:
		if quantity_try < 5:
			quantity_try+=1
			button1 = KeyboardButton('На сегодня')
			button2 = KeyboardButton('На завтра')
			button3 = KeyboardButton('На 3 дня')
			keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(button1, button2, button3)
			bot.send_message(message.chat.id, "ОШИБКА: укажите правильный формат")
			msg = bot.send_message(message.chat.id, "Выбери формат. Бот может прислать погоду на сегодня, на завтра или на 3 ближайших дня", reply_markup=keyboard)
			bot.register_next_step_handler(msg, add_format, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id, "Ты ошибся в заполнении, начни заново, выбери что ты хочешь, выбери /sub_weather или /unsubs_weather")


def add_time(message, user_info, quantity_try):
	if re.search(r'^[0-9]{2}:[0-59]{2}$', message.text) != None:
		user_info.append(message.text)
		connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
		request_insert_user_id = f"INSERT INTO subs_weather (id_user, city_weather, link, format, time) VALUES ('{user_info[0]}','{user_info[2]}','{user_info[3]}','{user_info[4]}');"
		insert_user_id = execute_query(connection, request_insert_user_id)
		bot.send_message(message.chat.id, "Ваша подписака добавлена в БД. Увидеть текущие подписки можно командой /my_sub_weather")
	else:
		if quantity_try < 5:
			quantity_try+=1
			bot.send_message(message.chat.id, "ОШИБКА: укажите правильный формат времени")
			msg = bot.send_message(message.chat.id, "Укажите время в формате чч:мм")
			bot.register_next_step_handler(msg, add_time, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id,"Ты ошибся в заполнении, начни заново, выбери что ты хочешь, выбери /sub_weather или /unsubs_weather")

bot.infinity_polling()


