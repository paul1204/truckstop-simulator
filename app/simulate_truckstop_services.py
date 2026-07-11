import threading
import multiprocessing

from app.merchandise.order.inventory_readings import simulate_order_inventory
from fuel.simulate_fuel import simulate_fuel_pump_sale
from app.merchandise.delivery.simulate_merchandise_delivery import simulate_merchandise_delivery
from parking_reservation.simulate_parking import simulate_parking_reservation
from restaurant_delivery.simulate_restaurant import simulate_restaurant_delivery
from house_accounts.charge_house_accounts import charge_house_accounts

def init():
    simulations = [
        simulate_order_inventory,
        simulate_fuel_pump_sale,
        simulate_merchandise_delivery,
        simulate_parking_reservation,
        simulate_restaurant_delivery,
        charge_house_accounts()
    ]

    # --- Multiprocessing Implementation ---
    processes = []

    for simulate_func in simulations:
        # Each simulation now runs in its own dedicated system process
        p = multiprocessing.Process(target=simulate_func)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # --- Threading Implementation (Commented out) ---
    # threads = []
    # for simulate_func in simulations:
    #     thread = threading.Thread(target=simulate_func)
    #     thread.start()
    #     threads.append(thread)
    #
    # for thread in threads:
    #     thread.join()

if __name__ == "__main__":
    init()