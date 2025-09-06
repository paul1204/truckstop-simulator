#!/usr/bin/env python3
"""
Configuration settings for the gas station shift report generator.
Adjust these values as needed for your specific setup.
"""

# Employee and Manager Configuration
TOTAL_EMPLOYEES = 12
TOTAL_MANAGERS = 2
SHIFTS_PER_DAY = 4

# Manager IDs (can be adjusted)
MANAGER_IDS = [100, 101]

# Employee ID range (starts from 1)
EMPLOYEE_ID_RANGE = list(range(1, TOTAL_EMPLOYEES + 1))

# Shift Configuration
SHIFT_TYPES = {
    1: "Morning",      # 6 AM - 12 PM
    2: "Midday",       # 12 PM - 6 PM  
    3: "Evening",      # 6 PM - 12 AM
    4: "Late Night"    # 12 AM - 6 AM
}

# API Configuration
DEFAULT_API_BASE_URL = "http://localhost:8080/api/shiftProcessing"

# Month names for user selection
MONTHS = {
    "JAN": "January",
    "FEB": "February", 
    "MAR": "March",
    "APR": "April",
    "MAY": "May",
    "JUN": "June",
    "JUL": "July",
    "AUG": "August",
    "SEP": "September",
    "OCT": "October",
    "NOV": "November",
    "DEC": "December"
}

# Default year range
from datetime import datetime
DEFAULT_YEAR = datetime.now().year
MIN_YEAR = 2020
MAX_YEAR = datetime.now().year