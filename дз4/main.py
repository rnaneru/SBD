import random
import uuid
from pprint import pprint
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
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

    def get_paid_subscribers_by_city(self, city: str) -> List[Dict[str, Any]]:
        pipeline = [
            {
                "$match": {
                    "person_data.city": city,
                    "person_data.features_paid_subscriptions": True
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "person_data.name": 1,
                    "person_data.age": 1,
                    "purchase_data.shop_id": 1
                }
            }
        ]
        return list(self.collection.aggregate(pipeline))

    def get_shop_operations_analytics(self, limit: int = 5) -> List[Dict[str, Any]]:
        pipeline = [
            {
                "$group": {
                    "_id": "$purchase_data.shop_id",
                    "total_operations": {"$sum": 1},
                    "unique_cities": {"$addToSet": "$person_data.city"}
                }
            },
            {"$sort": {"total_operations": -1}},
            {"$limit": limit}
        ]
        return list(self.collection.aggregate(pipeline))

    def check_index_usage(self, city: str) -> Dict[str, Any]:
        pipeline = [
            {"$match": {
                "person_data.city": city,
                "person_data.features_paid_subscriptions": True
            }}
        ]
        return self.collection.aggregate(pipeline, explain=True)


def generate_test_collection(
        connection_string: str = 'mongodb://localhost:27017/',
        db_name: str = 'hw',
        collection_name: str = 'hw4',
        object_sum: int = 5000) -> None:
    with MongoClient(connection_string) as client:
        db = client[db_name]
        collection = db[collection_name]

        collection.create_index([("person_data.city", ASCENDING)], name="idx_city")

        collection.create_index(
            [("person_data.city", ASCENDING), ("person_data.features_paid_subscriptions", ASCENDING)],
            name="idx_city_subscription"
        )

        collection.create_index([("purchase_data.shop_id", ASCENDING)], name="idx_shop_id")

        for i in range(object_sum):
            purchase_id = str(uuid.uuid4())

            data = {
                "operation_number": i,
                "person_data": {
                    "name": faker.name(),
                    "age": faker.random_int(8, 100),
                    "country": faker.country(),
                    "city": faker.city(),
                    "features_paid_subscriptions": faker.boolean(),
                },
                "purchase_data": {
                    "shop_id": faker.random_int(1, 50),
                    "item_id": faker.random_int(1, 100),
                }
            }

            collection.update_one(
                {"_id": purchase_id},
                {"$set": data},
                upsert=True
            )

        print(f"Generated and saved {object_sum} documents with indexes.")


if __name__ == "__main__":
    print("Starting data generation...")
    generate_test_collection(object_sum=1000)

    print("Initializing MongoDB client...")
    db_client = MongoDBClient()

    sample_city = faker.city()
    subscribers = db_client.get_paid_subscribers_by_city(sample_city)
    print(f"Found {len(subscribers)} subscribers in {sample_city}")
    if subscribers:
        pprint(subscribers[:2])

    print("Top shops analytics:")
    top_shops = db_client.get_shop_operations_analytics(limit=3)
    pprint(top_shops)

    print("Checking index usage plan:")
    explain_result = db_client.check_index_usage(sample_city)

    try:
        winning_plan = explain_result['stages'][0]['$cursor']['queryPlanner']['winningPlan']
        index_name = explain_result['stages'][0]['$cursor']['queryPlanner']['winningPlan'].get('indexName',
                                                                                               'Not specified')
        stage_type = winning_plan.get('stage', 'Not specified')

        print(f"Scan type: {stage_type}")
        print(f"Used index: {index_name}")

        if stage_type == 'IXSCAN':
            print("SUCCESS: Query uses index (IXSCAN).")
        else:
            print("WARNING: Index is not used.")
    except KeyError:
        print("Could not parse explain result.")

    db_client.close_connection()
    print("Connection closed.")
