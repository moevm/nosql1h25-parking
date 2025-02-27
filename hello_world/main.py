import pymongo

# подключаемся к клиенту
client = pymongo.MongoClient("localhost", 27017)

# создание базы данных и колекции
db = client['test']
collection = db['test']

# Запись данных
collection.drop()
collection.insert_one({"data": "Hello World!"})
# извлекаем данные из коллекций

# Поиск данных
print(collection.find_one())