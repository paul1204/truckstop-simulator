import requests


def get_all_merchandise():
    url = "http://localhost:8080/api/inventory/allMerchandise"
    response = requests.get(url)

    if response.status_code == 200:
        # Saving the list in a variable
        merchandise_list = response.json()
        return merchandise_list
    else:
        print(f"Failed to fetch merchandise: {response.status_code}")
        return []


def get_inventory_data():
    base_url = "http://localhost:8080/api/inventory"
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
    url = "http://localhost:8080/api/inventory/bottledBeverages"
    response = requests.get(url)
    data = response.json() if response.status_code == 200 else []

    for item in data:
        item['salesType'] = 'BOTTLED_BEVERAGE'
    return data


def get_packaged_food():
    url = "http://localhost:8080/api/inventory/packagedFood"
    response = requests.get(url)
    data = response.json() if response.status_code == 200 else []

    for item in data:
        item['salesType'] = 'PACKAGED_FOOD'
    return data

def simulate_order_inventory():
    """Function to be called by the main simulator"""
    print('----')
    bottled_beverages = get_bottled_beverages()
    packaged_food = get_packaged_food()
    print(f"Inventory Loaded: {len(bottled_beverages)} beverages, {len(packaged_food)} food items.")
    print(bottled_beverages)
    print(packaged_food)
    print('----')

if __name__ == "__main__":
    simulate_order_inventory()

# if __name__ == "__main__":
#     inventory = get_inventory_data()
#     print(inventory)
#     print(f"Loaded {len(inventory)} items into memory.")
#
#     # Saving lists in variables in memory
#     bottled_beverages = get_bottled_beverages()
#     packaged_food = get_packaged_food()
#
#     if bottled_beverages:
#         print(f"Example Beverage: {bottled_beverages[2]}")