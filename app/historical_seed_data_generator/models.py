"""
Data models representing sales and sales item records.
"""

from dataclasses import dataclass
from enum import IntEnum

class SalesType(IntEnum):
    FUEL = 0
    MERCHANDISE = 1

@dataclass
class SaleRecord:
    sales_id: str
    sales_amount: float
    sales_date: str          # Format: YYYY-MM-DD
    sales_time: str          # Format: HH:MM:SS
    shift_number: int        # 1 to 4
    terminal: str            # e.g., 'pump1'

@dataclass
class SalesItemRecord:
    id: str
    item_name: str           # e.g., 'Fuel'
    quantity: float          # e.g., gallons sold
    sales_type: int          # 0 for Fuel, 1 for Merchandise
    sku_code: str            # e.g., '87', 'Diesel'
    unit_price: float        # price per unit
    sales_id: str            # Foreign key referencing SaleRecord.sales_id
