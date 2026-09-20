import json

from faker import Faker

fake = Faker('ru_RU')

data = []
for _ in range(100):
    user = {
        "Имя": fake.name(),
        "Email": fake.email(),
        "Телефон": fake.phone_number(),
        "Город": fake.city(),
    }
    data.append(user)

with open('users_data.json', mode='w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)