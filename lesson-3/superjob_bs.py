# Собрать информацию о вакансиях на вводимую должность с сайта
# superjob.ru. Приложение должно анализировать несколько страниц сайта.
# Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (дополнительно: разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# cайт, откуда собрана вакансия.

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def get_info():
    vacancies_info_list = []
    len_data = 0
    for count in range(1, 6):
        sleep(1)
        url = f'https://www.superjob.ru/vakansii/analitik-dannyh.html?noGeo=1&page={count}'
        response = requests.get(url=url, headers=headers)
        soup = bs(response.text, 'html.parser')
        data = soup.find_all('div', {'class': "_2lp1U _2J-3z _3B5DQ"})
        len_data += len(data)
        for i in data:
            vacancy_tittle = i.find('a', {'target': "_blank"}).text
            vacancy_link = 'https://www.superjob.ru' + i.find('a', {'target': "_blank"}).get('href')
            vacancy_salary = i.find('span', {'class': "_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi"}).text
            try:
                vacancy_company = i.find('span', {
                    'class': "_3nMqD f-test-text-vacancy-item-company-name _2FkKs _249GZ _1jb_5 _1dIgi _3qTky"}).text
            except:
                vacancy_company = 'не указана'
            try:
                company_link = 'https://www.superjob.ru' + i.find('a', {'target': "_self"}).get('href')
            except:
                company_link = 'не указана'
            try:
                company_town = i.find('div', {'class': "_3gyJS eOMxK _3JTbG"}).text
            except:
                company_town = 'не указан'
            vacancy_dict = {'tittle': vacancy_tittle,
                            'link': vacancy_link,
                            'salary': vacancy_salary,
                            'company': vacancy_company,
                            'town': company_town,
                            'company_link': company_link,
                            'source': 'superjob.ru'
                            }
            vacancies_info_list.append(vacancy_dict)
    return (vacancies_info_list)


result_list = get_info()
for el in result_list:
    el['currency'] = el['salary'].split('\xa0')[-1]
    el['salary'] = el['salary'].replace('\xa0', '')

for el in result_list:
    if el['salary'] == 'По договорённости':
        el['min_salary'] = 'нет'
        el['max_salary'] = 'нет'
        el['currency'] = 'нет'
    elif el['salary'].startswith('от'):
        el['min_salary'] = el['salary'].replace('от', '')
        el['min_salary'] = int(el['min_salary'].replace(el['currency'], ''))
        el['max_salary'] = 'нет'
    elif el['salary'].startswith('до'):
        el['min_salary'] = 'нет'
        el['max_salary'] = el['salary'].replace('до', '')
        el['max_salary'] = int(el['max_salary'].replace(el['currency'], ''))
    else:
        el['min_salary'] = int(el['salary'].split('—')[0].replace(el['currency'], ''))
        el['max_salary'] = int(el['salary'].split('—')[-1].replace(el['currency'], ''))

data = pd.DataFrame(result_list)
with open(r'D:\vacancies.csv', 'w') as f:
    data.to_csv(f, sep=";", index=False)
