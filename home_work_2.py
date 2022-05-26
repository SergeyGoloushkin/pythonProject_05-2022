import requests
from pymongo import MongoClient
import pandas as pd
from bs4 import BeautifulSoup as bs
from pprint import pprint

main_url = 'https://hh.ru'
vacancy = input('Input vacancy_ ')
page = 0
all_vacancies = []
params = {'text': vacancy,
          'area': 1,
          'experience': 'doesNotMatter',
          'order_by': 'relevance',
          'search_period': 0,
          'items_on_page': 20,
          'page': page,}
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
        vacancy_company = vacancy_company_name.getText().replace('\xa0', ' ')
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

#df = pd.DataFrame(all_vacancies)
#df.to_csv('vacancy_file.csv', index=False, header=False) # >>> если нужно сохранить в csv формате

client = MongoClient('localhost', 27017)
vacancy_hh_db = client.vacancy_hh_db

for vacancy in all_vacancies:
    vacancy_hh_db.vacancy_hh.update_one({'link': vacancy['link']},
                                        {'$setOnInsert': {'company': vacancy['company'],
                                                          'currency': vacancy['currency'],
                                                          'max_salary': vacancy['max_salary'],
                                                          'min_salary': vacancy['min_salary'],
                                                          'name': vacancy['name'],
                                                          'site': vacancy['site']}},
                                        upsert=True)
salary = int(input('Input value for salary_ '))

search_salary = vacancy_hh_db.all_vacancies.find({'$or': [{'min_salary': {'$gt': salary}},
                                                          {'max_salary': {'$gt': salary}},]})
for item in search_salary:
    pprint(item)

# vacancy_hh_db.vacancy_hh.drop()