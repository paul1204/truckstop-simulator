import threading
from fuel.simulate_fuel import simulate_fuel_pump_sale
from merchandise.simulate_merchandise import simulate_merchandise_delivery
from parking_reservation.simulate_parking import simulate_parking_reservation
from restaurant_delivery.simulate_restaurant import simulate_restaurant_delivery

def init():
    # Define the simulation functions to run
    simulations = [
        simulate_fuel_pump_sale,
        simulate_merchandise_delivery,
        simulate_parking_reservation,
        simulate_restaurant_delivery
    ]

    threads = []

    # Create and start a thread for each simulation
    for simulate_func in simulations:
        thread = threading.Thread(target=simulate_func)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    init()