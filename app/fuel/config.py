import random
MAX_FUEL_GALLONS = 150.00
#DD/MM/YYYY
START_DATE = "01/03/2025"
# Shifts 1, 2, 3, or 4
START_SHIFT = 1

regular_octane_price = 3.80
num_pumps=15

FUEL_PRICES = {
    "diesel": 4.50,
    "regular": regular_octane_price,
    "premium": regular_octane_price + 0.50
}

FUEL_CONFIG = {
    "diesel": {
        "NUM_REQUESTS": 100,
        "INTERVAL_SECONDS": random.randint(1, 5),
        "OCTANE": 0,
        "PRICE_PER_GALLON": FUEL_PRICES["diesel"]
    },
    "regular": {
        "NUM_REQUESTS": 100,
        "INTERVAL_SECONDS": random.randint(1, 5),
        "OCTANE": 87,
        "PRICE_PER_GALLON": FUEL_PRICES["regular"]
    },
    "premium": {
        "NUM_REQUESTS": 100,
        "INTERVAL_SECONDS": random.randint(1, 5),
        "OCTANE": 93,
        "PRICE_PER_GALLON": FUEL_PRICES["premium"]
    }
} 