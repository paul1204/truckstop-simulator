from .pump_diesel_fuel import pump_diesel_fuel
from .pump_regular_fuel import pump_regular_fuel
from .pump_premium_fuel import pump_premium_fuel

def simulate_fuel_pump_sale():
    next_time = pump_diesel_fuel()
    next_time = pump_regular_fuel(start_time=next_time)
    pump_premium_fuel(start_time=next_time)
