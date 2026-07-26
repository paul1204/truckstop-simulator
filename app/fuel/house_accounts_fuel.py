import time

import requests
import json

from app.api_config import GET_ACCOUNTS_URL, PUT_FUEL_URL_TEMPLATE

def simulate_house_accounts_fuel():
    try:
        print(f"Fetching house accounts from {GET_ACCOUNTS_URL}...")
        response = requests.get(GET_ACCOUNTS_URL)
        print(response)
        if response.status_code != 200:
            print(f"Failed to fetch house accounts. Status: {response.status_code}")
            return

        house_accounts = response.json()
        print(f"Found {len(house_accounts)} house accounts.")

        payload = {
            "octane": 40,
            "gallonsSold": 1000,
            "totalPrice": 50.99,
            "specialMessage": "house account fuel simulation",
            "terminal": "house-account-terminal"
        }

        for account in house_accounts:
            account_id = account.get("houseAccountId")
            company_name = account.get("companyName", "Unknown")
            print(f"Account: {account_id} ({company_name})")
            
            if not account_id:
                print("Skipping account without houseAccountId")
                continue

            url = PUT_FUEL_URL_TEMPLATE.format(houseAccountId=account_id)
            print(f"Updating fuel for {company_name} ({account_id})...")
            
            put_response = requests.put(url, json=payload, headers={"Content-Type": "application/json"})
            time.sleep(2)
            if put_response.status_code == 200:
                print(f"  Successfully updated fuel for {account_id}")
            else:
                print(f"  Failed to update fuel for {account_id}. Status: {put_response.status_code}, Response: {put_response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    simulate_house_accounts_fuel()
