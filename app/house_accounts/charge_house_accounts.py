import random
import requests
import time
from app.house_accounts.get_house_accounts import get_house_accounts
from app.fuel.config import FUEL_PRICES

PATCH_FUEL_URL_TEMPLATE = "http://localhost:9000/truck-driver/fuel/update/Diesel/FIFO/HouseAccount/{houseAccountId}"
GET_STATUS_URL_TEMPLATE = "http://localhost:9000/accounting/house-accounts/{houseAccountId}/status"

def get_house_account_status(house_account_id):
    """
    Fetches the status of a specific house account.
    """
    url = GET_STATUS_URL_TEMPLATE.format(houseAccountId=house_account_id)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  Failed to fetch status for {house_account_id}. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"  Error fetching status for {house_account_id}: {e}")
        return None

def perform_fuel_charge(account_id, company_name, gallons_sold):
    """
    Makes a fuel charge for a house account.
    """
    diesel_price = FUEL_PRICES.get("diesel", 4.50)
    total_price = round(gallons_sold * diesel_price, 2)

    payload = {
        "octane": 40,  # Diesel usually doesn't have octane but following the requested schema
        "gallonsSold": gallons_sold,
        "totalPrice": total_price,
        "specialMessage": "House account fuel charge simulation",
        "terminal": f"Pump-{random.randint(1, 10)}"
    }

    url = PATCH_FUEL_URL_TEMPLATE.format(houseAccountId=account_id)
    print(f"Charging {company_name} ({account_id}) - {gallons_sold} gallons for ${total_price}...")

    try:
        response = requests.patch(url, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            print(f"  Successfully charged {account_id}")
            print(f"  Response: {response.json()}")
        else:
            print(f"  Failed to charge {account_id}. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"  Error charging {account_id}: {e}")

def charge_house_accounts():
    """
    Fetches house accounts and makes fuel charges to half of them.
    """
    print("Starting House Account Fuel Charge Simulation...")
    house_accounts = get_house_accounts()
    
    if not house_accounts:
        print("No house accounts found.")
        return

    # Select half per run
    num_to_charge = len(house_accounts) // 2
    if num_to_charge == 0 and len(house_accounts) > 0:
        num_to_charge = 1
        
    selected_accounts = random.sample(house_accounts, num_to_charge)
    print(f"Selecting {num_to_charge} house accounts to charge out of {len(house_accounts)}.")

    for account in selected_accounts:
        account_id = account.get("houseAccountId")
        company_name = account.get("companyName", "Unknown")
        
        if not account_id:
            print(f"Skipping account: {company_name} (No ID found)")
            continue

        # 1. Get status first
        status = get_house_account_status(account_id)
        if not status:
            print(f"  Could not retrieve status for {company_name}. Skipping charge.")
            continue

        credit_limit = status.get("creditLimit", 0.0)
        gallons_due = status.get("gallonsDue", 0.0)
        available_gallons = status.get("availableGallons", 0.0)

        # Calculate percentRemaining on the fly
        # If creditLimit is 0, we'll avoid division by zero
        percent_remaining = (available_gallons / credit_limit * 100) if credit_limit > 0 else 0.0

        print(f"  Account: {company_name} | Credit Limit: {credit_limit} | Gallons Due: {gallons_due} | "
              f"Available: {available_gallons} | Remaining: {percent_remaining:.2f}%")

        if available_gallons <= 0:
            print(f"  No available gallons for {company_name}. Skipping charge.")
            continue

        # 2. Generate random number between 1 and availableGallons
        gallons_sold = round(random.uniform(1.0, available_gallons), 2)
        
        # 3. Make the actual charge
        perform_fuel_charge(account_id, company_name, gallons_sold)
            
        # Small delay between requests
        time.sleep(1)

if __name__ == "__main__":
    charge_house_accounts()
