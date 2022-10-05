# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, которая будет добавлять только новые вакансии/продукты
# в вашу базу.
# Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой


import json
from pprint import pprint
from pymongo import MongoClient


def insert_data_to_mongo(data_list, collection):
    '''
        Функция вставляет новые данные в коллекцию (критерий отличия вакансий
        друг друга - несовпадение хотя бы одного параметра: названия вакансии,
        компания-работадатель, ссылка на вакансию).

        Параметры:
        data_list - список добавляемых вакансий;
        collection - коллекция, куда добавляются вакансии
    '''

    for item in data_list:
        item_tittle = item['tittle']
        item_company = item['company']
        item_link = item['link']
        collection.update_one({'tittle': item_tittle, 'company': item_company, 'link': item_link},
                              {'$set': item}, upsert=True)


def find_vacancies(collection):
    '''
        Функция производит поиск и выводит на экран вакансии
        с заработной платой больше введённой

        Параметры:
         collection - коллекция, в которой производится поиск
    '''

    user_salary = int(input("Введите желаемую зарплату: "))
    for item in collection.find({'$or': [{'max_salary': {'$gt': user_salary}},
                                         {'min_salary': {'$gt': user_salary}}]}):
        pprint(item)


with open(r'D:\vacancies.json', 'r', encoding='utf-8') as f:
    vacancies_info_list = json.load(f)

client = MongoClient('127.0.0.1:27017')
db = client['sj_vac']
vacancies = db.vacancies
insert_data_to_mongo(vacancies_info_list, vacancies)
find_vacancies(vacancies)
