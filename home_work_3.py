from pymongo import MongoClient
from pprint import pprint
from pymongo import DESCENDING
client = MongoClient('localhost', 27017)
print(client.list_database_names()) #посмотреть список баз данных

cars = [ {'name': 'Audi', 'price': 52642},
    {'name': 'Mercedes', 'price': 57127},
    {'name': 'Skoda', 'price': 9000},
    {'name': 'Volvo', 'price': 29000},
    {'name': 'Bentley', 'price': 350000},
    {'name': 'Citroen', 'price': 21000},
    {'name': 'Hummer', 'price': 41400},
    {'name': 'Volkswagen', 'price': 21600} ]

db = client.testdb  # создать базу данных с именем db
# db.cars.insert_many(cars)  # добавить в базу данных коллекцию cars
# print(db.list_collection_names()) # посмотреть все коллекции в созданной БД >>> cars
cars = db.cars.find() # переходим в коллекцию cars
# print(cars.next()) # выводит следующий элемент в коллекции

# pprint(list(cars)) # создает список из объектов коллекции

n_cars = len(list(db.cars.find()))
# print(f"There are {n_cars} cars")

cars = db.cars.find()
#for car in cars:
 #   print('{0} {1}'.format(car['name'],
  #      car['price']))

#expensive_cars = db.cars.find({'price': {'$gt': 50000}})
#for ecar in expensive_cars:
 #   print(ecar['name'])


#cars = db.cars.find({}, {'_id': 1, 'name':1})
#for car in cars:
 #   print(car)

# cars = db.cars.find().sort("price", DESCENDING)
# for car in cars:
   # print('{0} {1}'.format(car['name'],
    #    car['price']))

agr = [ {'$group': {'_id': 1, 'all': { '$sum': '$price' } } } ]
val = list(db.cars.aggregate(agr))
# print(val)

agr = [{ '$match': {'$or': [ { 'name': "Audi" }, { 'name': "Volvo" }] }},
    { '$group': {'_id': 1, 'sum2cars': { '$sum': "$price" } }}]
val = list(db.cars.aggregate(agr))
# print(val)

cars = db.cars.find().limit(8)
for car in cars:
    print('{0}: {1}'.format(car['name'], car['price']))

db.cars.drop()
