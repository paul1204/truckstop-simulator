from .config import FUEL_CONFIG, MAX_FUEL_GALLONS, START_DATE, START_SHIFT
import time
import requests
import random
from datetime import datetime, timedelta

from app.api_config import REGULAR_FUEL_URL as BACKEND_URL
from app.time_management.time_manager import get_simulated_time, is_simulation_finished, get_simulated_shift

NUM_REQUESTS = FUEL_CONFIG["regular"]["NUM_REQUESTS"]
INTERVAL_SECONDS = FUEL_CONFIG["regular"]["INTERVAL_SECONDS"]
OCTANE = FUEL_CONFIG["regular"]["OCTANE"]
PRICE_PER_GALLON = FUEL_CONFIG["regular"]["PRICE_PER_GALLON"]

def pump_regular_fuel(start_time=None):
    i = 0
    while not is_simulation_finished():
        try:
            # Generate random gallons sold (1 to MAX_FUEL_GALLONS)
            gallons_sold = round(random.uniform(1.0, MAX_FUEL_GALLONS), 2)
            
            # Calculate total price
            total_price = round(gallons_sold * PRICE_PER_GALLON, 2)
            
            current_time = get_simulated_time()
            shift_num = get_simulated_shift(current_time)
            
            payload = {
                "octane": OCTANE,
                "gallonsSold": gallons_sold,
                "totalPrice": total_price,
                "transactionDate": current_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "salesDate": current_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "date": current_time.strftime("%Y-%m-%d"),
                "daily_shift": shift_num,
                "specialMessage": "test",
                "terminal": "pump2"
            }
            
            print(f"Sending fuel pump simulation {i+1}...")
            print(f"  Time: {payload['transactionDate']}, Gallons: {gallons_sold}, Price per gallon: ${PRICE_PER_GALLON}, Total: ${total_price}")
            
            response = requests.put(BACKEND_URL, json=payload, headers={"Content-Type": "application/json"})
            print(f"Response: Status {response.status_code}, Body: {response.text}")
            
            i += 1

        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL_SECONDS)
    
    return get_simulated_time()

if __name__ == "__main__":
    pump_regular_fuel() 