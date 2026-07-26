import requests
from app.api_config import ALL_MERCHANDISE_URL, INVENTORY_BASE_URL, BOTTLED_BEVERAGES_URL, PACKAGED_FOOD_URL

def get_all_merchandise():
    url = ALL_MERCHANDISE_URL
    response = requests.get(url)

    if response.status_code == 200:
        # Saving the list in a variable
        merchandise_list = response.json()
        return merchandise_list
    else:
        print(f"Failed to fetch merchandise: {response.status_code}")
        return []

def get_inventory_data():
    base_url = INVENTORY_BASE_URL
    endpoints = [
      #  "/allMerchandise",
        "/bottledBeverages",
        "/packagedFood"
    ]

    all_inventory = []

    for endpoint in endpoints:
        response = requests.get(f"{base_url}{endpoint}")
        if response.status_code == 200:
            # Extending our list with the results from each endpoint
            all_inventory.extend(response.json())

    return all_inventory

def get_bottled_beverages():
    url = BOTTLED_BEVERAGES_URL
    response = requests.get(url)
    data = response.json() if response.status_code == 200 else []

    for item in data:
        item['salesType'] = 'BOTTLED_BEVERAGE'
    return data


def get_packaged_food():
    url = PACKAGED_FOOD_URL
    response = requests.get(url)
    data = response.json() if response.status_code == 200 else []

    for item in data:
        item['salesType'] = 'PACKAGED_FOOD'
    return data

def simulate_order_inventory():
    print('----')
    bottled_beverages = get_bottled_beverages()
    packaged_food = get_packaged_food()
    print(f"Inventory Loaded: {len(bottled_beverages)} beverages, {len(packaged_food)} food items.")
    print(bottled_beverages)
    print(packaged_food)
    print('----')

if __name__ == "__main__":
    simulate_order_inventory()