from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dbase import create_connection, execute_query, execute_read_query
def info_weather():
    # current_time = f'{str(datetime.now().hour)}:{str(datetime.now().minute)}'
    current_time = '10:00'
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
            elif element[4] == '3-days':
                values_list.append(parser_3days(element))
        return values_list
    else:
        return None


def parser_today(values:tuple):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    link = f'{values[3]}{values[4]}'
    html_doc = requests.get(link, headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {'user_id':values[1], 'city':values[2]}
    value_time_filter = []
    value_icon_filter = []
    value_temp_filter = []
    value_time = info.find('div', class_="widget-row widget-row-time")
    value_icon = info.find('div', class_="widget-row widget-row-icon")
    value_temp = info.find_all('span', class_="unit unit_temperature_c")
    for x in value_time:
        z = str(x.span.text).zfill(4)[0:2] + ':00'
        value_time_filter.append(z)
    for x in value_icon:
        if x.div['data-text'] == 'Пасмурно, небольшой  дождь':
            z = 'Дождь'
            value_icon_filter.append(z)
        elif x.div['data-text'] == 'Пасмурно,  дождь':
            z = 'Дождь'
            value_icon_filter.append(z)
        elif x.div['data-text'] == 'Пасмурно, небольшие  осадки':
            z = 'Осадки'
            value_icon_filter.append(z)
        elif x.div['data-text'] == 'Малооблачно, небольшой  снег с дождём':
            z = 'Дождь'
            value_icon_filter.append(z)
        else:
            z = x.div['data-text']
            value_icon_filter.append(z)
    for x in value_temp:
        value_temp_filter.append(x.text)
    value_temp_filter = value_temp_filter[6:]
    for i in range(8):
        dict1 = {value_time_filter[i]: {'time': value_time_filter[i], 'icon': value_icon_filter[i],'temp': value_temp_filter[i]}}
        weather_dict.update(dict1)
    return weather_dict

def parser_tomorrow(values:tuple):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    link = f'{values[3]}{values[4]}'
    html_doc = requests.get(link, headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {'user_id':values[1], 'city':values[2]}
    value_tomorrow = info.find('div', class_="weathertab-wrap")
    temp_min_max = value_tomorrow.find_all('span', class_='unit unit_temperature_c')
    weather_dict.update({'t_max': temp_min_max[1].text, 't_min':temp_min_max[0].text})
    return weather_dict


info_weather()