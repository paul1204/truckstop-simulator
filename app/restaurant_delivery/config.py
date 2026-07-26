#!/usr/bin/env python3
"""
Configuration for the restaurant delivery invoice sender.
Adjust INTERVAL_SECONDS to control the pause between requests.
"""
from pathlib import Path

# Endpoint configuration
from app.api_config import RESTAURANT_DELIVERY_URL as API_URL

# Form field name expected by the backend (per API contract)
FORM_FIELD_NAME = "merchandiseRestaurantOrder"

# Directory containing the CSV invoices to send
DELIVERY_INVOICE_DIR = Path(__file__).parent / "delivery_invoice"

# Interval (in seconds) between sending each CSV file
INTERVAL_SECONDS = 3
