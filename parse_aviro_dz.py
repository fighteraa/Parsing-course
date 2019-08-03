# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные объявления с avito.ru в созданную БД (xpath/BS для парсинга на выбор)

# 2) Написать функцию, которая производит поиск и выводит на экран объявления с ценой меньше введенной суммы


import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pprint


def connct_mongodb():
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['adverts']
    return db.adverts


def request_to_site():
    try:
        request = requests.get('https://www.avito.ru/sankt-peterburg/bytovaya_elektronika?p=1')
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def save_to_mongo_db():
    adverts_db = connct_mongodb()
    adverts_db.drop()

    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')

    all_adverts = soup.findAll('div', 'item_table-wrapper')
    for advert in all_adverts:
        try:
            price = advert.find("span", {"class": "price"}).contents[0]
            if ' ' in price[2:-2]:
                thing_price = price[2:-2].replace(" ", "")
                if not thing_price.isdigit():
                    thing_price = 0
            elif price[2:-2].isdigit():
                thing_price = price[2:-2]
            else:
                thing_price = 0
        except AttributeError:
            thing_price = 0
        try:
            div = advert.find('div', class_='data')
            metro = div.find_all("p")[-1].text.strip().replace(u'\xa0', ' ')
        except:
            metro = 'Метро не указанно'
        try:
            div = advert.find('div', class_='description').find('h3')
            url_advert = "https://avito.ru" + div.find("a").get("href")
        except:
            url_advert = 'Cсылка не найдена'

        data_advert = {
            "thing": advert.find("span", {"itemprop": "name"}).string,
            "price": int(thing_price),
            "metro": metro,
            "url": url_advert
        }
        adverts_db.insert_one(data_advert)


def find_price_less():
    save_to_mongo_db()

    adverts_db = connct_mongodb()

    less_price = int(input('Введите максимальную цену: '))
    for post in adverts_db.find({"$and": [{"price": {"$gt": 0}}, {"price": {"$lt": less_price}}]}).sort("price"):
        pprint.pprint(post)
        print('-' * 100)


find_price_less()
