import datetime
import time

import gspread
import pandas as pd

from database import add_line, create_table, delete_table

E1 = "стоимость в руб."
# Узнаем сегодняшнюю дату
dt = datetime.datetime.now()


def get_dollar():
    # Преобразовываем дату к виду dd/mm/yyyy
    dt_string = dt.strftime("%d/%m/%Y")
    # указываем url котировок с внесением сегодняшней даты
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={dt_string}"
    # получаем котировки через pd
    df = pd.read_xml(url, encoding='cp1251')
    # парсим доллар
    dollar = df.iloc[10]["Value"]
    dollar = float(dollar.replace(",", '.'))
    return dollar


# Указываем путь к JSON
gc = gspread.service_account(filename='enhanced-oasis.json')

# Открываем тестовую таблицу
sh = gc.open("test")

# Записываем заголовки в переменные
A1 = sh.sheet1.get('A1')[0][0]
B1 = sh.sheet1.get('B1')[0][0]
C1 = sh.sheet1.get('C1')[0][0]
D1 = sh.sheet1.get('D1')[0][0]

# записываем лист в переменную
worksheet = sh.sheet1


# запись из таблицы в базу данных построчно
def adding_records():
    dollar = get_dollar()
    # Забираем содержимое таблицы в список списков
    list_of_lists = worksheet.get_all_values()
    for i, j, k, l in list_of_lists:
        try:
            m = str(int(k) * dollar)
            add_line(i, j, k, l, m)

        except ValueError:
            pass


def main():
    delete_table()
    create_table()
    add_line(A1, B1, C1, D1, E1)
    adding_records()


if __name__ == '__main__':
    while True:
        main()
        print(f'<<<Таблица обновлена: {dt}>>>')
        time.sleep(30)
