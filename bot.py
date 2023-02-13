from dbase import create_connection, execute_query, execute_read_query
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import re
import telebot


def keyboard_inline():
	button1 = InlineKeyboardButton(text='Создать рассылку', callback_data='sub_weather')
	button2 = InlineKeyboardButton(text='Мои рассылки', callback_data='my_weather')
	button3 = InlineKeyboardButton(text='Удалить рассылку', callback_data='delete_weather')
	keyboard_inline = InlineKeyboardMarkup().row(button1).row(button2).row(button3)
	return keyboard_inline


bot = telebot.TeleBot("5644371123:AAERZpN6VG5xijGF2CZUvr2DjY97w7gLxko")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Привет, бот позволяет создать, посмотреть или удалить рассылки на погоду.\nВыбери что ты хочешь сделать:", reply_markup=keyboard_inline())


@bot.callback_query_handler(func=lambda call: call.data == 'sub_weather')
def sub_weather(call):
	user_info = []
	quantity_try = 0
	user_info.append(call.from_user.id)
	msg = bot.send_message(call.message.chat.id, "Напишите свой город")
	bot.register_next_step_handler(msg, add_city, user_info, quantity_try)

@bot.callback_query_handler(func=lambda call: call.data == 'my_weather')
def my_weather(call):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_value = f"select * from subs_weather where id_user={str(call.from_user.id)};"
	subs_weather = execute_read_query(connection, select_value)
	subs_weather_str = 'Твои текущие рассылки:\n\n'
	if len(subs_weather) == 0:
		bot.send_message(call.message.chat.id, "У тебя еще нет подписок на погоду")
	else:
		for value in subs_weather:
			day = str()
			if value[4] == 'today':
				day = 'сегодня'
			elif value[4] == 'tomorrow':
				day = 'завтра'
			subs_weather_str += f"№{str(value[0])}, {str(value[2])}, {day}, {str(value[5])}\n"
		bot.send_message(call.message.chat.id, subs_weather_str)

@bot.callback_query_handler(func=lambda call: call.data == 'delete_weather')
def delete_weather(call):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_value = f"select * from subs_weather where id_user={str(call.from_user.id)};"
	subs_weather = execute_read_query(connection, select_value)
	subs_weather_str = 'Твои текущие рассылки:\n\n'
	if len(subs_weather) == 0:
		bot.send_message(call.message.chat.id, "У тебя еще нет подписок на погоду")
	else:
		for value in subs_weather:
			day = str()
			if value[4] == 'today':
				day = 'сегодня'
			elif value[4] == 'tomorrow':
				day = 'завтра'
			subs_weather_str += f"№{str(value[0])}, {str(value[2])}, {day}, {str(value[5])}\n"
		subs_weather_str += f"\nУкажи номер рассылки, которую необходимо удалить:"
		msg = bot.send_message(call.message.chat.id, subs_weather_str)
		bot.register_next_step_handler(msg, delete_weather_sql)

def delete_weather_sql(message):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	request_insert_user_id = f"DELETE FROM subs_weather WHERE num={message.text} and id_user='{message.from_user.id}';"
	insert_user_id = execute_query(connection, request_insert_user_id)
	bot.send_message(message.chat.id, "Подписка удалена.", reply_markup=keyboard_inline())



def add_city(message, user_info, quantity_try):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_city = f"select * from cities where city='{str(message.text).title()}';"
	city = execute_read_query(connection, select_city)
	if len(city)==1:
		user_info.append(city[0][1])
		user_info.append(city[0][4])
		button1 = KeyboardButton('На сегодня')
		button2 = KeyboardButton('На завтра')
		keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(button1, button2)
		msg = bot.send_message(message.chat.id, "Выбери формат. Бот может прислать погоду на сегодня или на завтра", reply_markup=keyboard)
		bot.register_next_step_handler(msg, add_format, user_info, quantity_try)
	elif len(city)>1:
		city_name = str(message.text).title()
		city_str = 'Найдено несколько городов с такм именем. Укажите номер подходящего города из списка:\n'
		for x in city:
			city_str += f"*{str(x[0])}*" +' - '+ str(x[1]) +', '+ str(x[2]) + "\n"
		msg=bot.send_message(message.chat.id, city_str, parse_mode="Markdown")
		bot.register_next_step_handler(msg, check_city, user_info, quantity_try, city_name)
	elif len(city) == 0:
		if quantity_try < 5:
			quantity_try+=1
			bot.send_message(message.chat.id, "ОШИБКА: Такого города нет в базе данных!")
			msg = bot.send_message(message.chat.id, "Напишите свой город")
			bot.register_next_step_handler(msg, add_city, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id, "Ты ошибся в заполнении, начни заново",reply_markup=keyboard_inline())


def check_city(message, user_info, quantity_try, city_name):
	connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
	select_city = f"select * from cities where number='{message.text}' and city='{city_name}';"
	city = execute_read_query(connection, select_city)
	if len(city) == 1:
		user_info.append(city[0][1])
		user_info.append(city[0][4])
		button1 = KeyboardButton('На сегодня')
		button2 = KeyboardButton('На завтра')
		keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(button1, button2)
		msg = bot.send_message(message.chat.id, "Выбери формат. Бот может прислать погоду на сегодня или на завтра.", reply_markup=keyboard)
		bot.register_next_step_handler(msg, add_format, user_info, quantity_try)
	else:
		if quantity_try < 5:
			quantity_try += 1
			bot.send_message(message.chat.id, "ОШИБКА: Такого города нет в базе данных!")
			msg = bot.send_message(message.chat.id, "Напишите свой город")
			bot.register_next_step_handler(msg, add_city, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id, "Ты ошибся в заполнении, начни заново.", reply_markup=keyboard_inline())



def add_format(message, user_info, quantity_try):
	if message.text == 'На сегодня':
		user_info.append('today')
		msg = bot.send_message(message.chat.id, "Укажите время в формате ЧЧ:ММ. Например 08:05 или 21:30", reply_markup=ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, add_time, user_info, quantity_try)
	elif message.text == 'На завтра':
		user_info.append('tomorrow')
		msg = bot.send_message(message.chat.id, "Укажите время в формате ЧЧ:ММ. Например 08:05 или 21:30", reply_markup=ReplyKeyboardRemove())
		bot.register_next_step_handler(msg, add_time, user_info, quantity_try)
	else:
		if quantity_try < 5:
			quantity_try+=1
			button1 = KeyboardButton('На сегодня')
			button2 = KeyboardButton('На завтра')
			keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(button1, button2)
			bot.send_message(message.chat.id, "ОШИБКА: укажите правильный формат")
			msg = bot.send_message(message.chat.id, "Выбери формат. Бот может прислать погоду на сегодня или на завтра.", reply_markup=keyboard)
			bot.register_next_step_handler(msg, add_format, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id, "Ты ошибся в заполнении, начни заново.", reply_markup=keyboard_inline())


def add_time(message, user_info, quantity_try):
	if re.search(r'^(([0,1][0-9])|(2[0-3])):[0-5][0-9]$', message.text) != None:
		user_info.append(message.text)
		connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
		request_insert_user_id = f"INSERT INTO subs_weather (id_user, city_weather, link, format, time) VALUES ('{user_info[0]}','{user_info[1]}','{user_info[2]}','{user_info[3]}','{user_info[4]}');"
		insert_user_id = execute_query(connection, request_insert_user_id)
		bot.send_message(message.chat.id, "Ваша подписака добавлена в БД.", reply_markup=keyboard_inline())
	else:
		if quantity_try < 5:
			quantity_try+=1
			bot.send_message(message.chat.id, "ОШИБКА: укажите правильный формат времени")
			msg = bot.send_message(message.chat.id, "Укажите время в формате ЧЧ:ММ. Например 08:05 или 21:30")
			bot.register_next_step_handler(msg, add_time, user_info, quantity_try)
		else:
			bot.send_message(message.chat.id,"Ты ошибся в заполнении, начни заново.", reply_markup=keyboard_inline())



if __name__ == '__main__':
	bot.infinity_polling()


