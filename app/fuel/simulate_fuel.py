import threading
import random

from .config import num_pumps
from .pump_diesel_fuel import pump_diesel_fuel
from .pump_regular_fuel import pump_regular_fuel
from .pump_premium_fuel import pump_premium_fuel

def run_pump(pump_id):
    fuel_types = [pump_diesel_fuel, pump_regular_fuel, pump_premium_fuel]
    fuel_func = random.choice(fuel_types)
    print(f"Pump {pump_id} starting with {fuel_func.__name__}")
    fuel_func()

def simulate_fuel_pump_sale():
    threads = []
    for i in range(num_pumps):
        thread = threading.Thread(target=run_pump, args=(i+1,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
