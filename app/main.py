from pump_diesel_fuel import pump_diesel_fuel
from pump_regular_fuel import pump_regular_fuel
from pump_premium_fuel import pump_premium_fuel
import threading

def main():
    pump_diesel_fuel()
    pump_regular_fuel()
    pump_premium_fuel()

if __name__ == "__main__":
    main() 