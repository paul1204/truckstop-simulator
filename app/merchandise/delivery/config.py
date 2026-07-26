#!/usr/bin/env python3
"""
Configuration for the merchandise delivery invoice sender.
Adjust INTERVAL_SECONDS to control the pause between requests.
"""
from pathlib import Path

# Endpoint configuration
API_URL = "http://localhost:9000/api/inventory/delivery/merchandise"

# Form field name expected by the backend
FORM_FIELD_NAME = "merchandiseInventoryOrder"

# Directory containing the CSV invoices to send
DELIVERY_INVOICE_DIR = Path(__file__).parent / "delivery_invoice"

# Interval (in seconds) between sending each CSV file
INTERVAL_SECONDS = 2

DATE = "01/02/2024"