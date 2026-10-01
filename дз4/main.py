import random, uuid

from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import objectid
from typing import List, Dict, Any
from faker import Faker

faker = Faker('ru_RU')


class MongoDBClient:
    def __init__(self,
                 db_name: str = 'hw',
                 collection_name: str = 'hw4',
                 connection_string: str = 'mongodb://localhost:27017/'):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def close_connection(self):
        self.client.close()






def generate_test_collection(
        connection_string: str = 'mongodb://localhost:27017/',
        db_name: str = 'hw',
        collection_name: str = 'hw4',
        object_sum: int = 5000) -> None:
    with MongoClient(connection_string) as client:
        db = client[db_name]
        collection = db[collection_name]

        for i in range(object_sum):
            purchase = str(uuid.uuid4())

            data = {
                "operation_number": i,
                "person_data": {
                    "name": faker.name(),
                    "age": faker.random_int(8, 100),
                    "country": faker.country(),
                    "city": faker.city(),
                    "features_paid_subscriptions": faker.boolean(),},

                "purchase_data": {
                    "shop_id": faker.random_int(1, 50),
                    "item_id": faker.random_int(1, 100),
                }
            }

            collection.update_one(
                {"_id": purchase},
                {"$set": data},
                upsert=True)

generate_test_collection()