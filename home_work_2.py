"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
получаем должность) с сайтов HH(обязательно). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv."""

import requests
import json
import pandas as pd
import csv
from bs4 import BeautifulSoup as bs
from pprint import pprint
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
main_url = 'https://hh.ru'
vacancy = input('Введите название вакансии_ ')
page = 0
all_vacancies = []
params = {'text': vacancy,
          'area': 1,
          'experience': 'doesNotMatter',
          'order_by': 'relevance',
          'search_period': 0,
          'items_on_page': 20,
          'page': page}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         'AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/98.0.4758.141 YaBrowser/22.3.4.731 Yowser/2.5 Safari/537.36'}
response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'html.parser')
try:
    last_page = int(soup.find_all('a',{'data-qa':'pager-page'})[-1].text)
except:
    last_page = 1

for i in range(last_page):

    soup = bs(response.text, 'html.parser')

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies:

        vacancy_info = {}
        vacancy_anchor = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"})
        vacancy_name = vacancy_anchor.getText()
        vacancy_info['name'] = vacancy_name

        vacancy_link = vacancy_anchor['href']
        vacancy_info['link'] = vacancy_link

        vacancy_company_name = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-employer"})
        vacancy_company = vacancy_company_name.getText()
        vacancy_info['company'] = vacancy_company

        vacancy_info['site'] = main_url + '/'

        vacancy_salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if vacancy_salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            vacancy_salary = vacancy_salary.getText()
            if vacancy_salary.startswith('РґРѕ'):
                max_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                min_salary = None
                currency = vacancy_salary.split()[-1]

            elif vacancy_salary.startswith('РѕС‚'):
                max_salary = None
                min_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

            else:
                max_salary = int("".join([s for s in vacancy_salary.split('вЂ“')[0] if s.isdigit()]))
                min_salary = int("".join([s for s in vacancy_salary.split('вЂ“')[0] if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

        vacancy_info['max_salary'] = max_salary
        vacancy_info['min_salary'] = min_salary
        vacancy_info['currency'] = currency

        all_vacancies.append(vacancy_info)

    params['page'] += + 1
    response = requests.get(main_url + '/search/vacancy', params=params, headers=headers)

df = pd.DataFrame(all_vacancies)
df.to_csv('vacancy_file.csv', index=False, header=False)

















