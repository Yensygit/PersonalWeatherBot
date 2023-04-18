from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dbase import create_connection, execute_read_query


def info_weather():
    """
    Функция формирует запрос в БД по текущему времени. Если в БД имеются значения,
    передает их в нужную функцию, для формирования данных о погоде.

    :return: Словарь с данными о погоде если в БД имеются значения.
             None в случае если значений в БД нет
    """
    time = datetime.now()
    # time = datetime(year=2023, month=2, day=17, hour=13, minute=2, second=12)
    current_time = time.strftime('%H:%M')
    connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
    select_value_db = f"select * from subs_weather where time='{current_time}';"
    value_db = execute_read_query(connection, select_value_db)
    values_list = []
    if len(value_db) > 0:
        for element in value_db:
            if element[4] == 'today':
                values_list.append(parser_today(element))
            elif element[4] == 'tomorrow':
                values_list.append(parser_tomorrow(element))
        return values_list
    else:
        return None


def parser_today(values:tuple):
    """
    Парсит страницу Gismeteo на основе параметров полученных из функции 'info_weather'

    :return: Словарь с данными о погоде если в БД имеются значения.

    """
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    link = f'{values[3]}'
    html_doc = requests.get(link, headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {'user_id': values[1], 'city': values[2]}
    value_today = info.find('a', class_="weathertab weathertab-block tooltip")
    wind = info.find_all('span', class_='wind-unit unit unit_wind_m_s')
    wind_list = [int(i.text[0]) for i in wind]
    if len(wind_list)>0:
        wind_max = max(wind_list)
    else:
        wind_max = 'Безветренно'
    temp_min_max = value_today.find_all('span', class_='unit unit_temperature_c')
    day = value_today.find('div', class_='tab-content')
    day_text = day.contents[0].text
    condition = value_today.attrs['data-text']
    weather_dict.update({'t_max': temp_min_max[1].text, 't_min': temp_min_max[0].text, 'day': day_text, 'format': 'Завтра','condition': condition, 'wind_max': wind_max})
    return weather_dict

def parser_tomorrow(values:tuple):
    """
    Парсит страницу Gismeteo на основе параметров полученных из функции 'info_weather'

    :return: Словарь с данными о погоде если в БД имеются значения.

    """
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    link = f'{values[3]}{values[4]}'
    html_doc = requests.get(link, headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {'user_id':values[1], 'city':values[2]}
    value_tomorrow = info.find('a', class_="weathertab weathertab-block tooltip")
    wind = info.find_all('span', class_='wind-unit unit unit_wind_m_s')
    wind_list = [int(i.text) for i in wind]
    if len(wind_list)>0:
        wind_max = max(wind_list)
    else:
        wind_max = 'Безветренно'
    wind_max = max(wind_list)
    temp_min_max = value_tomorrow.find_all('span', class_='unit unit_temperature_c')
    day = value_tomorrow.find('div', class_='tab-content')
    day_text = day.contents[0].text
    condition = value_tomorrow.attrs['data-text']
    weather_dict.update({'t_max': temp_min_max[1].text, 't_min':temp_min_max[0].text, 'day':day_text, 'format':'Завтра', 'condition':condition, 'wind_max':wind_max})
    return weather_dict
