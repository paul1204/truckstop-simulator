# Configuration for fuel pump simulations

# Global fuel settings
MAX_FUEL_GALLONS = 150.00  # Maximum gallons that can be sold per transaction

# Starting date and shift for simulation
# Date format: DD/MM/YYYY
START_DATE = "01/03/2025"
# Shift can be 1, 2, 3, or 4
START_SHIFT = 1

# Price per gallon for each fuel type
regular_octane_price = 3.80

FUEL_PRICES = {
    "diesel": 4.50,
    "regular": regular_octane_price,
    "premium": regular_octane_price + 0.50
}

FUEL_CONFIG = {
    "diesel": {
        "NUM_REQUESTS": 100,
        "INTERVAL_SECONDS": 1,
        "OCTANE": 0,
        "PRICE_PER_GALLON": FUEL_PRICES["diesel"]
    },
    "regular": {
        "NUM_REQUESTS": 100,
        "INTERVAL_SECONDS": 1,
        "OCTANE": 87,
        "PRICE_PER_GALLON": FUEL_PRICES["regular"]
    },
    "premium": {
        "NUM_REQUESTS": 100,
        "INTERVAL_SECONDS": 1,
        "OCTANE": 93,
        "PRICE_PER_GALLON": FUEL_PRICES["premium"]
    }
} 