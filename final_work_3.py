# ИМПОРТИРУЕМ МОДУЛИ

import csv  # для работы с csv файлами
import requests  # для работы со ссылками
from datetime import datetime  # для работы с датами и временем
import matplotlib.pyplot as plt  # для работы с визуализациями


# ФУНКЦИИ

def read_sales_data(responce):
    '''Принимает ссылку к файлу и возвращает список продаж'''
    sales_data = []  # объявляем список для заполнения
    if responce.status_code == 200:  # проверяем успешен ли HTTP-запрос
        content = responce.content.decode('utf-8').splitlines()  # то что получили декодируется в UTF-8 и разбивается на строки
        reader = csv.reader(content, delimiter=',')  # создаем объект который будет читать строки, разделитель запятая
        for row in reader:  # проходим по каждой строке
            product_name, quantity, price, date = row  # определяем значения для каждой записи в строке
            # создаем словарь и добавляем его в список sales_data
            sales_data.append({
                'product_name': str(product_name),
                'quantity': int(quantity),
                'price': int(price),
                'date': datetime.strptime(date.strip(), '%Y-%m-%d')
            })
    return sales_data  # отдаем заполненный список

def total_sales_per_product(sales_data):
    '''Принимает список продаж, а возвращает словарь, где ключ название продукта, значение - общая сумма по продукту'''
    total_sales = {}  # объявляем словарь для заполнения
    for sale in sales_data:
        product = sale['product_name']  # получаем название продукта
        total = sale['quantity'] * sale['price']  # перемножаем между собой количество и цену
        if product in total_sales:  # проверяем если в словаре total_sales есть продукт
            total_sales[product] += total  # прибавляем к его значению данные из строки
        else:  # если продукта в словаре нет, то
            total_sales[product] = total  # создается новая запись в словаре с названием м суммой
    return total_sales  # отдаем заполненный словарь

def sales_over_time(sales_data):
    '''Принимает список продаж, а возвращает словарь, где ключ дата, значение - общая сумма по дате'''
    sales_by_date = {}  # объявляем словарь для заполнения
    for sale in sales_data:
        date = sale['date']  # получаем даты
        total = sale['quantity'] * sale['price']  # перемножаем между собой количество и цену
        if date in sales_by_date:  # проверяем если в словаре есть дата, то
            sales_by_date[date] += total  # прибавляем к ее значению данные из строки
        else:  # если даты нет в словаре, то
            sales_by_date[date] = total  # создается новая запись в словаре с названием и суммой
    return sales_by_date  # отдаем заполненный словарь



# РАСЧЕТ ПОКАЗАТЕЛЕЙ

# Переменная для ссылки на файл с данными, можно поставить свою ссылку
url = 'https://raw.githubusercontent.com/TheBony/final_work_3/main/data.csv'

# Забираем данные по ссылке
responce = requests.get(url)

# Список с продажами
sales_data = read_sales_data(responce)

# Словарь с общей суммой продаж по продуктам
total_sales = total_sales_per_product(sales_data)

# Словарь с общей суммой продаж по дням
sales_by_date = sales_over_time(sales_data)

# Определяем наибольшую выручку по продукту
best_product = max(total_sales.values())  # определяем максимальное значение
best_product_name = [k for k, v in total_sales.items() if v == best_product][0]  # определяем ключ максимального значения

# Определяем наибольшую выручку по дате
best_sales_by_date = max(sales_by_date.values())  # определяем максимальное значение
best_sales_by_date_date = [k for k, v in sales_by_date.items() if v == best_sales_by_date][0]  # определяем ключ максимального значения



# СТРОИМ ГРАФИКИ

fig, axs = plt.subplots(1, 2, figsize=(16, 9))  # определяем два графика на одном холсте

# График с общей суммой по продуктам
axs[0].bar(total_sales.keys(), total_sales.values(), color='skyblue')  # по оси х продукт по оси y общая сумма по продукту
axs[0].bar(best_product_name, best_product, color='dodgerblue')  # изменяем цвет столбца для максимального значения
axs[0].set_title('Общая сумма продаж по каждому продукту')  # добавляем название к графику

# График с общей суммой по дням
axs[1].bar(sales_by_date.keys(), sales_by_date.values(), color='limegreen')  # по оси х даты по оси y общая сумма по датам
axs[1].bar(best_sales_by_date_date, best_sales_by_date, color='forestgreen')  # изменяем цвет столбца для максимального значения
axs[1].set_title('Общая сумма продаж по дням')   # добавляем название к графику
axs[1].tick_params(axis='x', rotation=45)  # подписи оси х делаем под 45 градусов

# Итоги по анализу добавляем к холсту с графиками
fig.suptitle(f'ИТОГИ АНАЛИЗА ДАННЫХ.\n\n'
             f'Наибольшую выручку принес продукт: "{best_product_name}" - {best_product}.\n'
             f'Наибольшая выручка была получена: {datetime.date(best_sales_by_date_date)} - {best_sales_by_date}.',
             fontsize=16,
             ha='left',
             x=0.034)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # учитываем пространство для suptitle
plt.show()  # выводим графики
