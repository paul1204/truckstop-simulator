"""
Configuration settings for the Historical Seed Data Generator.
Easily customize time ranges, record counts, batching, terminals, and fuel pricing.
"""

# ==============================================================================
# Date & Time Range Configuration
# ==============================================================================
# Available month options (copy-pasteable):
# "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
START_MONTH = "Jan"
END_MONTH = "Dec"
YEAR = 2026


# ==============================================================================
# Volume & SQL Dialect Configuration
# ==============================================================================
# Total sales records to distribute across the calendar days of the range
TOTAL_RECORDS = 200000

# Batch size: number of row values grouped under a single INSERT statement
BATCH_SIZE = 500

# SQL dialect prefix for multi-row inserts (use "INSERT IGNORE INTO" for idempotent dev runs)
SQL_INSERT_PREFIX = "INSERT IGNORE INTO"

# File write mode:
# "overwrite" = creates fresh .sql files on each run
# "append"    = appends new batch to existing .sql files (to stack up records across multiple runs)
FILE_WRITE_MODE = "overwrite"

# Output directory root for generated SQL files
OUTPUT_SQL_DIR = "sql"

# ==============================================================================
# Locations & Terminals Configuration
# ==============================================================================
# List of store locations (currently 1, easily expandable: ["1"], ["A001", "B002", "C003"])
LOCATIONS = ["1"]

# Explicit terminal pumps
TERMINALS = ["pump1", "pump2", "pump3", "pump4"]

# ==============================================================================
# Fuel Products Configuration
# ==============================================================================
# Pricing and gallon fill ranges per fuel type
FUEL_CONFIG = {
    "87": {
        "item_name": "Regular Fuel",
        "unit_price": 3.29,
        "min_gallons": 10.0,
        "max_gallons": 25.0,
        "sales_type": 0,
    },
    "93": {
        "item_name": "Premium Fuel",
        "unit_price": 3.89,
        "min_gallons": 10.0,
        "max_gallons": 25.0,
        "sales_type": 0,
    },
    "Diesel": {
        "item_name": "Diesel",
        "unit_price": 5.79,
        "min_gallons": 40.0,
        "max_gallons": 120.0,
        "sales_type": 0,
    },
}
