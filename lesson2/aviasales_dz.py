# Задание 1. Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
# а не по IATA коду. Пункт отправления и пункт назначения должны передаваться в качестве параметров.
# Сделать форматированный вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета,
# цену билета (можно добавить еще другие параметры по желанию)

import sys

import requests
import pprint
import json


def tickets_for_cities(from_city, to_city):
    print("Выполняется поиск по Вашему запросу\n\n")
    flight_city = "https://www.travelpayouts.com/widgets_suggest_params?q=Из%20" + from_city + "%20в%20" + to_city

    try:
        city = requests.get(flight_city)
    except requests.exceptions.URLRequired:
        print("ConnectionError!")

    data = city.json()

    try:
        flight_params = {
            'origin': data['origin']['iata'],
            'destination': data['destination']['iata'],
            'one_way': 'true'
        }
        req = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
    except KeyError:
        print("Таких городов нет в базе. Проверьте введенные данные! ")
        sys.exit(0)
    except requests.exceptions.ConnectionError:
        print("ConnectionError!")

    data_tickets = req.json()
    tickets = data_tickets['best_prices']
    for ticket in tickets:
        print(f'Пункт отправления {from_city}\nПункт назначения: {to_city}')
        print(f'Дата вылета {ticket["depart_date"]} \nЦена билета: {ticket["value"]} р.')
        print('-' * 50)


# tickets_for_cities("Санкт-Петербург", "Москва")

if __name__ == '__main__':
    tickets_for_cities(sys.argv[1], sys.argv[2])
