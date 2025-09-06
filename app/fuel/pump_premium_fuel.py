from config import FUEL_CONFIG
import time
import requests

BACKEND_URL = "http://localhost:8080/fuel/update/PremiumFuel/FIFO"

payload = {
    "octane": 91,
    "gallonsSold": 1500.00,
    "totalPrice": 39.99,
    "specialMessage": "test"
}

NUM_REQUESTS = FUEL_CONFIG["premium"]["NUM_REQUESTS"]
INTERVAL_SECONDS = FUEL_CONFIG["premium"]["INTERVAL_SECONDS"]

def pump_premium_fuel():
    for i in range(NUM_REQUESTS):
        try:
            print("Sending fuel pump simulation...")
            response = requests.put(BACKEND_URL, json=payload, headers={"Content-Type": "application/json"})
            print(f"Response: Status {response.status_code}, Body: {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    pump_premium_fuel() 