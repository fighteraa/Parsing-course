# Задание 2. В приложении парсинга википедии получить первую
# ссылку на другую страницу и вывести все значимые слова из неё.
# Результат записать в файл в форматированном виде

import collections
import requests
import re
import sys


def return_wiki_html(topic):
    try:
        wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
        wiki_request.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f'В википедии нет данных о слове: {topic}')
        sys.exit(0)

    text_split_links = wiki_request.text.split('</span><span class="mw-headline" id="Ссылки">Ссылки</span>')
    text_split_html_links = text_split_links[1].split('<ul><li><a rel="nofollow" ')
    text_links = text_split_html_links[1].split('</li></ul>')
    links = re.findall('(href=[\'"])(.+?)[\'"]', text_links[0])

    first_link = requests.get(f'{links[0][1]}')
    first_link.encoding = 'utf-8'
    return first_link.text


def return_words(topic):
    first_link_wiki_html = return_wiki_html(topic)
    words = re.findall('[а-яА-Я]{3,}', first_link_wiki_html)
    words_counter = collections.Counter(words)

    for word in words_counter.most_common(10):
        print(f'Слово {word[0]} встречается {word[1]} раз')
    my_file = open(f'{topic}.txt', "w+")
    for word in words_counter.most_common(10):
        print(f'Слово {word[0]} встречается {word[1]} раз')
        my_file.write(f'Слово {word[0]} встречается {word[1]} раз\n')
    my_file.close()

    return '\nПрограмма завершилась успешно'


# print(return_words('Физика'))
# print(return_words('Философия'))
# print(return_words('Физивапвапвапвапапка'))

if __name__ == '__main__':
    print(return_words(sys.argv[1]))
