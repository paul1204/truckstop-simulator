import requests
from app.shower.config import SHOWER_RESERVE_API_URL

def reserve_shower_unit(shower_number, customer_name, start_time, end_time):
    """
    Reserves a shower unit by calling the shower reservation endpoint.
    """
    payload = {
        "showerNumber": shower_number,
        "customerName": customer_name,
        "startTime": start_time,
        "endTime": end_time
    }
    
    try:
        response = requests.post(SHOWER_RESERVE_API_URL, json=payload)
        response.raise_for_status()
        print(f"Successfully reserved shower unit {shower_number} for {customer_name}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error reserving shower unit {shower_number}: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None
