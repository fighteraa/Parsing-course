# Задание:
# Найти все вакансии по двум профессиям и сравнить их средние значения.
# Сейчас в программе парсится по 8 страниц для каждой специальности, т.к. для программиста и инженера более 90 стр.

import requests
from bs4 import BeautifulSoup


def request_to_site(vacancy_name, page=0):
    headers = {
        'accept': '*/*',
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    params = {
        'text': vacancy_name,
        'page': page
    }
    try:
        request = requests.get('https://hh.ru/search/vacancy', headers=headers, params=params)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def get_total_pages(vacancy):
    html = request_to_site(vacancy)
    soup = BeautifulSoup(html, 'html.parser')
    total_pages = soup.findAll('a', class_='bloko-button HH-Pager-Control')[-1].get('data-page')
    return total_pages


def parse_vacancies(vacancy_name, page):
    all_salary = []
    html_doc = request_to_site(vacancy_name, page)
    soup = BeautifulSoup(html_doc, 'html.parser')
    vacancies = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacancy in vacancies:
        try:
            salary = vacancy.find('div', {'class': "vacancy-serp-item__compensation"}).string
            all_salary.append(salary)
        except AttributeError:
            pass

    return all_salary


def avarage_salary(name_vacancy):
    total_pages = 8
    # total_pages = int(get_total_pages(name_vacancy)) #Поиск на всех страницах
    total_salary = []

    for p in range(total_pages + 1):
        print(f'Сейчас парсится {p} страница вакансии "{name_vacancy}"')
        all_salary = parse_vacancies(name_vacancy, p)
        for salary in all_salary:
            salary = str(salary)
            if 'руб.' in salary and not 'бел' in salary:
                if 'от' in salary or 'до' in salary:
                    sal_transform = salary[2:-4].replace(" ", "")
                else:
                    sal_transform = (salary[:-4].replace(" ", ""))
                if '-' in sal_transform:
                    sal_aver_transf = sal_transform.split('-')
                    sal_aver = (int(sal_aver_transf[0]) + int(sal_aver_transf[1])) / 2
                    total_salary.append(sal_aver)
                else:
                    total_salary.append(int(sal_transform.replace(" ", "")))

    print('-' * 50)
    return sum(total_salary) / len(total_salary)


#Фиксированные данные
first_vacancy = 'Инженер'
secend_vacansy = 'Программист'

#Если раскомментировать, то можно вводить любые провессии
# first_vacancy = input('Введите первую вакансию: ')
# secend_vacansy = input('Введите вторую вакансию: ')

avg_first = avarage_salary(first_vacancy)
avg_second = avarage_salary(secend_vacansy)
print(f'Сердняя зарплата "{first_vacancy}" составляет {int(avg_first)} руб.')
print(f'Сердняя зарплата "{secend_vacansy}" составляет {int(avg_second)} руб.')
if avg_first > avg_second:
    print(f'Среднаяя зарпалата "{first_vacancy}" больше, чем средняя зарплата "{secend_vacansy}"')
else:
    print(f'Среднаяя зарпалата "{secend_vacansy}" больше, чем средняя зарплата "{first_vacancy}"')
