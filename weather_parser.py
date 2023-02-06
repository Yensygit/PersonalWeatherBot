import requests
from bs4 import BeautifulSoup
def info_dm():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    html_doc = requests.get('https://www.gismeteo.ru/weather-krasnodar-5136/tomorrow/', headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    weather_dict = {}
    value_time_filter = []
    value_icon_filter = []
    value_temp_filter = []
    value_time = info.find('div', class_="widget-row widget-row-time")
    value_icon = info.find('div', class_="widget-row widget-row-icon")
    value_temp = info.find_all('span', class_="unit unit_temperature_c")
    for x in value_time:
        z=str(x.span.text).zfill(4)[0:2]+':00'
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
            z=x.div['data-text']
            value_icon_filter.append(z)
    for x in value_temp:
        value_temp_filter.append(x.text)
    value_temp_filter = value_temp_filter[6:]
    for i in range(8):
        dict1 = {value_time_filter[i]:{'time':value_time_filter[i], 'icon':value_icon_filter[i], 'temp':value_temp_filter[i]}}
        weather_dict.update(dict1)
    return weather_dict