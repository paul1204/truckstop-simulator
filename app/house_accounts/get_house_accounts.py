import requests
import json

GET_ACCOUNTS_URL = "http://localhost:9000/accounting/house-accounts"

def get_house_accounts():
    """
    Fetches house accounts from the ERP backend, stores them in memory, and prints their values.
    """
    try:
        print(f"Fetching house accounts from {GET_ACCOUNTS_URL}...")
        response = requests.get(GET_ACCOUNTS_URL)
        
        if response.status_code != 200:
            print(f"Failed to fetch house accounts. Status: {response.status_code}")
            return None

        # Pull them and place them in memory
        house_accounts = response.json()
        
        if not house_accounts:
            print("No house accounts found.")
            return house_accounts

        print(f"Successfully retrieved {len(house_accounts)} house accounts:\n")
        
        # Print the values
        for account in house_accounts:
            print("-" * 40)
            for key, value in account.items():
                print(f"{key}: {value}")
        print("-" * 40)
        
        return house_accounts

    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the backend at {GET_ACCOUNTS_URL}. Is the Spring Boot app running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

if __name__ == "__main__":
    get_house_accounts()
