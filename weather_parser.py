from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dbase import create_connection, execute_read_query


def info_weather():
    current_time = f'{str(datetime.now().hour)}:{str(datetime.now().minute)}'
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
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    link = f'{values[3]}'
    html_doc = requests.get(link, headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {'user_id': values[1], 'city': values[2]}
    value_today = info.find('a', class_="weathertab weathertab-block tooltip")
    humidity = info.find_all('div', class_='widget-row widget-row-humidity')
    humidity_list = [int(i.text) for i in humidity[0].contents]
    humidity_average = sum(humidity_list) / len(humidity_list)
    wind = info.find_all('span', class_='wind-unit unit unit_wind_m_s')
    wind_list = [int(i.text) for i in wind[16:]]
    wind_max = max(wind_list)
    temp_min_max = value_today.find_all('span', class_='unit unit_temperature_c')
    day = value_today.find_all('div', class_='date date-1')
    condition = value_today.attrs['data-text']
    weather_dict.update({'t_max': temp_min_max[1].text, 't_min': temp_min_max[0].text, 'day': day[0].text, 'format': 'Завтра','condition': condition, 'humidity_average': humidity_average, 'wind_max': wind_max})
    return weather_dict

def parser_tomorrow(values:tuple):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    link = f'{values[3]}{values[4]}'
    html_doc = requests.get(link, headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {'user_id':values[1], 'city':values[2]}
    value_tomorrow = info.find('a', class_="weathertab weathertab-block tooltip")
    humidity = info.find_all('div', class_='widget-row widget-row-humidity')
    humidity_list = [int(i.text) for i in humidity[0].contents]
    humidity_average = sum(humidity_list)/len(humidity_list)
    wind = info.find_all('span', class_='wind-unit unit unit_wind_m_s')
    wind_list = [int(i.text) for i in wind[16:]]
    wind_max = max(wind_list)
    temp_min_max = value_tomorrow.find_all('span', class_='unit unit_temperature_c')
    day = value_tomorrow.find_all('div', class_='date date-2')
    condition = value_tomorrow.attrs['data-text']
    weather_dict.update({'t_max': temp_min_max[1].text, 't_min':temp_min_max[0].text, 'day':day[0].text, 'format':'Завтра', 'condition':condition, 'humidity_average':humidity_average, 'wind_max':wind_max})
    return weather_dict

info_weather()