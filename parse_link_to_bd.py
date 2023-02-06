from dbase import create_connection, execute_query
import requests
from bs4 import BeautifulSoup

"""Функция наполнения БД ссылками для каждого города с сайта Gismeteo"""
def parsing():
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    html_doc = requests.get('https://www.gismeteo.ru/catalog/russia/', headers=headers)
    info = BeautifulSoup(html_doc.text, 'html.parser')
    info_dict_global = []
    info_value = info.find_all('div', class_="catalog-item-link")
    print('Получение ссылок на регионы')
    for i in info_value:
        if 'link-popular' not in str(i):
            x=str(i).split('"')
            info_dict_global.append(f'https://www.gismeteo.ru{x[5]}')
    info_dict_district=[]
    print('Получение ссылок на районы')
    for x in info_dict_global:
        html_doc = requests.get(x, headers=headers)
        info = BeautifulSoup(html_doc.text, 'html.parser')
        info_value = info.find_all('div', class_="catalog-item-link")
        for i in info_value:
            if 'link-popular' not in str(i):
                x=str(i).split('"')
                info_dict_district.append(f'https://www.gismeteo.ru{x[5]}')
    print('Получение ссылок на населенные пункты и запись данных в БД')
    for x in info_dict_district:
        html_doc = requests.get(x, headers=headers)
        info = BeautifulSoup(html_doc.text, 'html.parser')
        info_value = info.find_all('div', class_="catalog-item-link")
        zone_regoin = info.find_all('a',class_="breadcrumbs-link")
        zone_district = info.find('a',class_="link subdistrict")
        for i in info_value:
            if 'link-popular' not in str(i):
                print(i)
                x=str(i).split('"')
                city = str(i.text).strip()
                link = f'https://www.gismeteo.ru{x[5]}'
                region = zone_regoin[2].text
                district = zone_district.text.replace(', ','')
                connection = create_connection("C:\Soft\Projects\PersonalWeatherBot\PWB_DB.sqlite")
                create_city = f'INSERT INTO cities (region, district, city, link) VALUES ("{region}","{district}","{city}","{link}");'
                execute_query(connection, create_city)
    return f'Выполнено'