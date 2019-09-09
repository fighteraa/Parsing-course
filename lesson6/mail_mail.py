import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver_firefox = webdriver.Chrome()
letters_list = []


def login_func(driver=driver_firefox):

    elem = driver.find_element_by_id('mailbox:login')
    elem.send_keys('example-for-geekbrains')

    elem = driver.find_element_by_id('mailbox:password')
    elem.send_keys('password-example')
    elem.send_keys(Keys.RETURN)
    time.sleep(1)
    assert 'Входящие' in driver.title
    print('Login success')

    time.sleep(1)


def collect_letters(driver=driver_firefox):
    elements = driver.find_elements_by_class_name('llc')
    print(f'Найдено писем на странице: {len(elements)}')
    if len(elements) == 0:
        print('Писем на странице не найдено')
        pass

    for i in range(1, len(elements)+1):
        elements = driver.find_elements_by_class_name('llc')
        correspondent = elements[-i].find_element_by_class_name('ll-crpt').get_attribute('title')
        letter_date = elements[-i].find_element_by_class_name('llc__item_date').get_attribute('title')
        letter_title = elements[-i].find_element_by_class_name('ll-sj__normal').text

        elements[-i].find_element_by_class_name('ll-sj__normal').click()
        time.sleep(1)
        letter_text = driver.find_element_by_css_selector('div.letter-body__body-wrapper table tbody').text

        driver.back()
        letters_list.append({'correspondent': correspondent,
                             'letter_date': letter_date,
                             'letter_title': letter_title,
                             'letter_text': letter_text, })
        time.sleep(1)


def save_to_mongo_db(letters_list, drop=True):
    from pymongo import MongoClient
    records_count = 0
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['letters']
    mailru_db = db.mailru

    if drop:
        mailru_db.drop()

    for letter in letters_list:
        mailru_db.insert_one(letter)
        records_count += 1
    print(f'{records_count} records added in MongoDB')


driver_firefox.get('https://mail.ru')
time.sleep(1)
assert 'почта, поиск' in driver_firefox.title

login_func()
collect_letters()

child_folders = driver_firefox.find_elements_by_css_selector('a.nav__item.nav__item_child.nav__item_expanded_true')
child_folders[0].click()
collect_letters()

child_folders[1].click()
collect_letters()

print(f'Всего собрано писем: {len(letters_list)}')

save_to_mongo_db(letters_list, drop=True)
