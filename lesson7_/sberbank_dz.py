# Создать приложение, которое будет из готового файла с данными «Сбербанка»
# (https://www.sberbank.com/ru/analytics/opendata) выводить результат по параметрам:
# • Тип данных
# • Интервал дат
# • Область
# Визуализировать выводимые данные с помощью графика


import matplotlib.pyplot as plt
import csv
import datetime

with open('opendata.csv', 'r') as f:
    type_of_data = 'Средняя зарплата'
    start_data = datetime.datetime.strptime('2015-02-15', "%Y-%m-%d")
    end_data = datetime.datetime.strptime('2018-12-15', "%Y-%m-%d")
    select_ragion = 'Челябинская область'
    reader = csv.DictReader(f)
    field_names = reader.fieldnames
    print(field_names)
    money = []
    date = []
    ragion = []

    for row in reader:
        row['date'] = datetime.datetime.strptime(row['date'], "%Y-%m-%d")
        if row['name'] == type_of_data and row['region'] == select_ragion and row['date'] > start_data \
                and row['date'] < end_data:
            date.append(row['date'])
            money.append(int(row['value']))

plt.plot(date, money)
plt.show()
