import requests
import random
import time

URL = "http://ml_service:8000/api/prediction/{item_id}"

# Пример данных (можно заменить на генератор или загрузку из файла)

import random

def generate_random_example():
    selling_types = ["Individual", "Dealer"]
    transmissions = ["Manual", "Automatic"]
    fuel_types = ["Petrol", "Diesel", "CNG"]

    example = {
        "Driven_kms": random.randint(10000, 150000),
        "Fuel_Type": random.choice(fuel_types),
        "Selling_type": random.choice(selling_types),
        "Transmission": random.choice(transmissions),
        "Owner": random.randint(0, 3),
        "Age_of_car": random.randint(1, 25),
        "Car_depreciation": round(random.uniform(5.0, 25.0), 3)
    }

    return example

def send_request(item_id: int):
    try:
        response = requests.post(URL.format(item_id=item_id), json=generate_random_example())
        print(f"[{item_id}] Status: {response.status_code}, Response: {response.json()}")
    except Exception as e:
        print(f"[{item_id}] Request failed: {e}")

def run():
    item_id = 1
    while True:
        send_request(item_id)
        item_id += 1
        sleep_time = random.uniform(0, 5)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    run()
