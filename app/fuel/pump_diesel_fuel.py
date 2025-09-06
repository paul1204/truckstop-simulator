from config import FUEL_CONFIG, MAX_FUEL_GALLONS
import time
import requests
import random

BACKEND_URL = "http://localhost:8080/fuel/update/Diesel/FIFO"

NUM_REQUESTS = FUEL_CONFIG["diesel"]["NUM_REQUESTS"]
INTERVAL_SECONDS = FUEL_CONFIG["diesel"]["INTERVAL_SECONDS"]
OCTANE = FUEL_CONFIG["diesel"]["OCTANE"]
PRICE_PER_GALLON = FUEL_CONFIG["diesel"]["PRICE_PER_GALLON"]

def pump_diesel_fuel():
    for i in range(NUM_REQUESTS):
        try:
            # Generate random gallons sold (1 to MAX_FUEL_GALLONS)
            gallons_sold = round(random.uniform(1.0, MAX_FUEL_GALLONS), 2)
            
            # Calculate total price
            total_price = round(gallons_sold * PRICE_PER_GALLON, 2)
            
            payload = {
                "octane": OCTANE,
                "gallonsSold": gallons_sold,
                "totalPrice": total_price,
                "specialMessage": "test"
            }
            
            print(f"Sending fuel pump simulation {i+1}/{NUM_REQUESTS}...")
            print(f"  Gallons: {gallons_sold}, Price per gallon: ${PRICE_PER_GALLON}, Total: ${total_price}")
            
            response = requests.put(BACKEND_URL, json=payload, headers={"Content-Type": "application/json"})
            print(f"Response: Status {response.status_code}, Body: {response.text}")
        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    pump_diesel_fuel() 