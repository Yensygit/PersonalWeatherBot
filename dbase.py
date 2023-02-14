import sqlite3
from sqlite3 import Error

def create_connection(path):
    """
    Создание подключения к БД

    :param path: Путь к БД
    :return: Возвращает объект подключения SQLite
    """
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    """
    Функция внесения изменений в БД

    :param connection: Объект подключения SQLite
    :param query: Запрос для БД
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    """
    Функция запроса данных из БД

    :param connection: Объект подключения SQLite
    :param query: Запрос для БД
    :return: Результат выполнения запроса к БД
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")