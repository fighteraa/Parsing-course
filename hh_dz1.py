# 1) Необходимо собрать информацию о вакансиях на должность
# программиста или разработчика с сайта job.ru или hh.ru.
# (Можно с обоих сразу) Приложение должно анализировать
# несколько страниц сайта. Получившийся список должен содержать в себе:
#
# *Наименование вакансии,
# *Предлагаемую зарплату
# *Ссылку на саму вакансию

# В программе реализован поиск по первым 5 страницам на сайте hh.ru

import requests
from lxml import html


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


def request_to_hh():
    all_page_req = []
    profession = 'Программист'
    session = requests.Session()

    for p in range(4):
        request = session.get('https://spb.hh.ru/search/vacancy', params={'text': profession, 'page': 1},
                              headers=headers)
        root = html.fromstring(request.text)
        results_list = root.xpath("//a[contains(@class, 'bloko-link HH-LinkModifier')]/text() "
                                  "| //div[contains(@class, 'vacancy-serp-item__compensation')]/text()"
                                  "| //a[contains(@class, 'bloko-link HH-LinkModifier')]/@href")
        all_page_req.extend(results_list)

    if all_page_req:
        f_posit = 0
        for k in range(len(all_page_req)):
            if f_posit == 0:
                print(f'Ссылка на вакансию: {all_page_req[k]}')
                f_posit = 1
            elif f_posit == 1:
                print(f'Наименование Вакансии: {all_page_req[k]}')
                if k < len(all_page_req) - 1:
                    if not all_page_req[k + 1].find('http'):
                        f_posit = 0
                        print(f'Зарплата: Не указана')
                        print('-' * 50)
                    else:
                        f_posit = 2
                        continue
            elif f_posit == 2:
                print(f'Зарплата: {all_page_req[k]}')
                print('-' * 100)
                f_posit = 0
    else:
        print("At your request no results were found. Please, check your request.")


request_to_hh()
