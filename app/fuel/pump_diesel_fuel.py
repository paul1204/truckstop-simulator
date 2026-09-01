from .config import FUEL_CONFIG, MAX_FUEL_GALLONS, START_DATE, START_SHIFT
import time
import requests
import random
from datetime import datetime, timedelta

from app.api_config import DIESEL_FUEL_URL as BACKEND_URL
from app.time_management.time_manager import get_simulated_time, is_simulation_finished, get_simulated_shift

NUM_REQUESTS = FUEL_CONFIG["diesel"]["NUM_REQUESTS"]
INTERVAL_SECONDS = FUEL_CONFIG["diesel"]["INTERVAL_SECONDS"]
OCTANE = FUEL_CONFIG["diesel"]["OCTANE"]
PRICE_PER_GALLON = FUEL_CONFIG["diesel"]["PRICE_PER_GALLON"]

def pump_diesel_fuel(start_time=None):
    i = 0
    while not is_simulation_finished():
        try:
            # Generate random gallons sold (50 to 200)
            gallons_sold = round(random.uniform(50.0, 200.0), 2)
            
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
                "dailyShift": shift_num,
                "specialMessage": "test",
                "terminal": "pump1"
            }
            
            print(f"Sending fuel pump simulation {i+1}...")
            print(f"  Time: {payload['transactionDate']}, Gallons: {gallons_sold}, Price per gallon: ${PRICE_PER_GALLON}, Total: ${total_price}")
            
            response = requests.put(BACKEND_URL, json=payload, headers={"Content-Type": "application/json"})
            print(f"Response: Status {response.status_code}, Body: {response.text}")
            
            print("Current simulated time:")
            print(current_time)

            i += 1

        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL_SECONDS)
    
    return get_simulated_time()

if __name__ == "__main__":
    pump_diesel_fuel() 