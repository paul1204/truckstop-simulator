from .send_reservations import reserve_all_spots


def simulate_parking_reservation():
    messages = reserve_all_spots()
    for idx, msg in enumerate(messages, start=1):
        print(f"[{idx}/10] {msg}")
    return messages