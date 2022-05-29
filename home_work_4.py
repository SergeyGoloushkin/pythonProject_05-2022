from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

url = 'https://yandex.ru/news/'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath(".//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top']")
list_items = []
for item in items:
    item_info = {}
    name = item.xpath(".//h2[@class='mg-card__title']/a/text()")
    link = item.xpath(".//h2[@class='mg-card__title']/a/@href")
    source = item.xpath(".//span[@class='mg-card-source__source']/a[last()]/text()")
    date = item.xpath(".//span[@class='mg-card-source__time']/text()")

    item_info['name'] = name
    item_info['link'] = link
    item_info['source'] = source
    item_info['date'] = date
    list_items.append(item_info)
#   Получается, что при формировании словаря, программа сгружает сразу в список все найденные значения
#   и присваивает весь список как одно значение для ключа. Можно было через костыли разобрать полученный словарь
#   и сделать правильный список со словарями по каждой новости, но подвох там в другом и, думаю,
#   решение именно в построении правильного xpath. Но как его сделать, чтобы все корректно выгружалось, так и не понял

pprint(list_items)

client = MongoClient('localhost', 27017)
yandex_news_db = client.yandex_news_db

for item in list_items:
    yandex_news_db.yandex_news.update_one({'link': list_items[0]['link']},
                                         {'$setOnInsert': {'date': list_items[0]['date'],
                                                           'name': list_items[0]['name'],
                                                           'source': list_items[0]['source']}},
                                         upsert=True)

pprint(list(yandex_news_db.yandex_news.find()))