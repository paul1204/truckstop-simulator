from config import FUEL_CONFIG
import time
import requests

BACKEND_URL = "http://localhost:8080/api/inventory/fuel/update/DieselFuel/FIFO"  # Update as needed

payload = {
    "octane": 0,  # Update as needed
    "gallonsSold": 10,  # example value
    "totalPrice": 39.99  # example value
}

NUM_REQUESTS = FUEL_CONFIG["diesel"]["NUM_REQUESTS"]
INTERVAL_SECONDS = FUEL_CONFIG["diesel"]["INTERVAL_SECONDS"]

def pump_diesel_fuel():
    for i in range(NUM_REQUESTS):
        try:
            print("Sending fuel pump simulation...")
            response = requests.put(BACKEND_URL, json=payload, headers={"Content-Type": "application/json"})
            print(f"Response: Status {response.status_code}, Body: {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    pump_diesel_fuel() 