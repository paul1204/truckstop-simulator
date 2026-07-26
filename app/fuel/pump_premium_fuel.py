from .config import FUEL_CONFIG, MAX_FUEL_GALLONS, START_DATE, START_SHIFT
import time
import requests
import random
from datetime import datetime, timedelta

BACKEND_URL = "http://localhost:9000/fuel/update/PremiumFuel/FIFO"

NUM_REQUESTS = FUEL_CONFIG["premium"]["NUM_REQUESTS"]
INTERVAL_SECONDS = FUEL_CONFIG["premium"]["INTERVAL_SECONDS"]
OCTANE = FUEL_CONFIG["premium"]["OCTANE"]
PRICE_PER_GALLON = FUEL_CONFIG["premium"]["PRICE_PER_GALLON"]

def pump_premium_fuel(start_time=None):
    # Parse START_DATE and START_SHIFT if no start_time provided
    if start_time is None:
        base_date = datetime.strptime(START_DATE, "%d/%m/%Y")
        # Shift 1: 00:00, Shift 2: 06:00, Shift 3: 12:00, Shift 4: 18:00
        start_hour = (START_SHIFT - 1) * 6
        current_time = base_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    else:
        current_time = start_time

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
                "transactionDate": current_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "salesDate": current_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "date": current_time.strftime("%Y-%m-%d"),
                "daily_shift": START_SHIFT,
                "specialMessage": "test",
                "terminal": "pump3"
            }
            
            print(f"Sending fuel pump simulation {i+1}/{NUM_REQUESTS}...")
            print(f"  Time: {payload['transactionDate']}, Gallons: {gallons_sold}, Price per gallon: ${PRICE_PER_GALLON}, Total: ${total_price}")
            
            response = requests.put(BACKEND_URL, json=payload, headers={"Content-Type": "application/json"})
            print(f"Response: Status {response.status_code}, Body: {response.text}")
            
            # Increment time for next request
            current_time += timedelta(seconds=random.randint(2, 3))

        except Exception as e:
            print(f"Error occurred: {e}")
        time.sleep(INTERVAL_SECONDS)
    
    return current_time

if __name__ == "__main__":
    pump_premium_fuel() 