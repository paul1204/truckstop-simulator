import random
import requests
import time
from app.house_accounts.get_house_accounts import get_house_accounts
from app.fuel.config import FUEL_PRICES

PATCH_FUEL_URL_TEMPLATE = "http://localhost:8080/truck-driver/fuel/update/Diesel/FIFO/HouseAccount/{houseAccountId}"

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

        # Generate some random fuel data
        gallons_sold = round(random.uniform(50.0, 300.0), 2)
        diesel_price = FUEL_PRICES.get("diesel", 4.50)
        total_price = round(gallons_sold * diesel_price, 2)
        
        payload = {
            "octane": 40, # Diesel usually doesn't have octane but following the requested schema
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
            
        # Small delay between requests
        time.sleep(1)

if __name__ == "__main__":
    charge_house_accounts()
