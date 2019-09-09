# 1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
#
# *Заголовок
# *Краткое описание
# *Ссылка на новость

import requests
from bs4 import BeautifulSoup


def request_to_site():
    try:
        request = requests.get('https://news.yandex.ru/Saint_Petersburg')

        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def parse_vacancies():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')

    tag_class_news = [{'class': 'story__topic'}, {'class': 'story story_view_normal'},
                      {'class': 'story story_view_short'}, {'class': 'story story_view_with-left-image'},
                      {'class': 'story story_view_normal story_noimage'}]

    for news_from_tag in tag_class_news:
        news = soup.findAll('div', news_from_tag)
        for i in news:
            print(f'Заголовок статьи: {i.find("a", {"link link_theme_black i-bem"}).string}')
            try:
                print(f'Описание статьи: {i.find("div", {"story__text"}).string}')
            except AttributeError:
                print('Описания нет')
            print(
                f'Ссылка на статью: {"https://news.yandex.ru/" + i.find("a", {"link link_theme_black i-bem"})["href"]}')
            print('-' * 100)


parse_vacancies()
