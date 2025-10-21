from app.parking_reservation.send_reservations import reserve_all_spots


def main():
    messages = reserve_all_spots()
    for idx, msg in enumerate(messages, start=1):
        print(f"[{idx}/10] {msg}")
    return messages

if __name__ == "__main__":
    main()
