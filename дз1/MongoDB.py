import json

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['test']
collection = db['users']



with open('users_data.json', mode='r', encoding='utf-8') as file:
    users = json.load(file)

for user in users:
    result = collection.insert_one(user)