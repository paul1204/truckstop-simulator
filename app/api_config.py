import os

# Central base URL for the backend Spring service
BACKEND_BASE_URL = os.getenv("SIMULATOR_BACKEND_URL", "http://localhost:9000")

# --- Fuel & House Accounts ---
GET_ACCOUNTS_URL = f"{BACKEND_BASE_URL}/accounting/house-accounts"
PUT_FUEL_URL_TEMPLATE = f"{BACKEND_BASE_URL}/truck-driver/fuel/update/Diesel/FIFO/HouseAccount/{{houseAccountId}}"
PATCH_FUEL_URL_TEMPLATE = f"{BACKEND_BASE_URL}/truck-driver/fuel/update/Diesel/FIFO/HouseAccount/{{houseAccountId}}"
GET_STATUS_URL_TEMPLATE = f"{BACKEND_BASE_URL}/accounting/house-accounts/{{houseAccountId}}/status"

DIESEL_FUEL_URL = f"{BACKEND_BASE_URL}/fuel/update/Diesel/FIFO"
PREMIUM_FUEL_URL = f"{BACKEND_BASE_URL}/fuel/update/PremiumFuel/FIFO"
REGULAR_FUEL_URL = f"{BACKEND_BASE_URL}/fuel/update/RegularFuel/FIFO"

# --- Merchandise ---
MERCHANDISE_DELIVERY_URL = f"{BACKEND_BASE_URL}/api/inventory/delivery/merchandise"
ALL_MERCHANDISE_URL = f"{BACKEND_BASE_URL}/api/inventory/allMerchandise"
INVENTORY_BASE_URL = f"{BACKEND_BASE_URL}/api/inventory"
BOTTLED_BEVERAGES_URL = f"{BACKEND_BASE_URL}/api/inventory/bottledBeverages"
PACKAGED_FOOD_URL = f"{BACKEND_BASE_URL}/api/inventory/packagedFood"
RESTAURANT_DELIVERY_URL = f"{BACKEND_BASE_URL}/api/inventory/delivery/restaurant"

# --- Parking ---
PARKING_RESERVE_URL = f"{BACKEND_BASE_URL}/api/parking/reserve"

# --- POS ---
POS_INGEST_SALES_URL = f"{BACKEND_BASE_URL}/pos-ingest/sales"

# --- Shift ---
SHIFT_PROCESSING_BASE_URL = f"{BACKEND_BASE_URL}/api/shiftProcessing"

# --- Shower ---
SHOWER_API_URL = f"{BACKEND_BASE_URL}/api/showers"
SHOWER_RESERVE_API_URL = f"{BACKEND_BASE_URL}/api/showers/reserve"
