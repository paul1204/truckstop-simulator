import requests
from app.shower.config import SHOWER_API_URL

def get_shower_units():
    """
    Fetches all shower units from the back end and stores them in memory.
    For now, it just prints them.
    """
    try:
        response = requests.get(SHOWER_API_URL)
        response.raise_for_status()
        shower_units = response.json()
        
        print("--- Shower Units ---")
        for unit in shower_units:
            print(unit)
        print("--------------------")
        
        return shower_units
    except requests.exceptions.RequestException as e:
        print(f"Error fetching shower units: {e}")
        return []

if __name__ == "__main__":
    get_shower_units()
