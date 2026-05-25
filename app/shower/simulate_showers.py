import time
import random
from datetime import datetime, timedelta
from app.shower.get_showers import get_shower_units
from app.shower.reserve_showers import reserve_shower_unit

def simulate_shower_activity():
    """
    Simulates shower activity. Fetches shower units and reserves a random half of them.
    """
    print("Starting Shower Simulation...")
    shower_units = get_shower_units()
    
    if not shower_units:
        print("No shower units found.")
        return

    # Reserve a random half of the shower units
    num_to_reserve = len(shower_units) // 2
    if num_to_reserve == 0 and len(shower_units) > 0:
        num_to_reserve = 1
        
    selected_units = random.sample(shower_units, num_to_reserve)
    print(f"Selecting {num_to_reserve} units to reserve out of {len(shower_units)}.")

    start_time = datetime.now().isoformat()
    end_time = (datetime.now() + timedelta(hours=1)).isoformat()

    for unit in selected_units:
        # Assuming unit has 'unitNumber' or 'showerNumber'.
        # We'll use 'showerNumber' if available, otherwise fallback to 'unitNumber' or 'id'.
        shower_number = str(unit.get('showerNumber', unit.get('unitNumber', unit.get('id', 'Unknown'))))
        customer_name = f"Customer-{random.randint(1000, 9999)}"
        
        reserve_shower_unit(
            shower_number=shower_number,
            customer_name=customer_name,
            start_time=start_time,
            end_time=end_time
        )

if __name__ == "__main__":
    simulate_shower_activity()
