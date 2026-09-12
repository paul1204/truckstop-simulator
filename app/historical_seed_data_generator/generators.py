"""
Data generation logic for historical truckstop sales.
Iterates across every calendar day in the configured range (daily grain)
and distributes sales across shifts, terminals, and fuel types.
"""

import calendar
import random
from datetime import date, time, datetime, timedelta
from typing import Dict, List, Tuple

from .config import (
    START_MONTH,
    END_MONTH,
    YEAR,
    TOTAL_RECORDS,
    LOCATIONS,
    TERMINALS,
    FUEL_CONFIG,
)
from .id_generator import generate_sale_id, generate_item_id
from .models import SaleRecord, SalesItemRecord, SalesType

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

MONTH_MAP = {name: i + 1 for i, name in enumerate(MONTH_NAMES)}
MONTH_REV_MAP = {i + 1: name for i, name in enumerate(MONTH_NAMES)}


def get_calendar_days(year: int, start_month_name: str, end_month_name: str) -> List[date]:
    """Return all calendar dates from the 1st of start_month to the last day of end_month."""
    start_m = MONTH_MAP[start_month_name]
    end_m = MONTH_MAP[end_month_name]

    days = []
    for m in range(start_m, end_m + 1):
        _, num_days = calendar.monthrange(year, m)
        for d in range(1, num_days + 1):
            days.append(date(year, m, d))
    return days


def distribute_counts_across_days(total_count: int, num_days: int) -> List[int]:
    """
    Distribute total_count across num_days with realistic small fluctuations,
    ensuring every day has at least 1 record and the sum equals total_count exactly.
    """
    if num_days <= 0:
        return []

    base = total_count // num_days
    remainder = total_count % num_days

    # Start with base counts
    counts = [base] * num_days

    # Add remainder evenly
    for i in range(remainder):
        counts[i] += 1

    # Add minor natural variance while maintaining exact sum
    if base > 4:
        for _ in range(num_days * 2):
            idx_from = random.randint(0, num_days - 1)
            idx_to = random.randint(0, num_days - 1)
            if idx_from != idx_to and counts[idx_from] > 5:
                shift_amount = random.randint(1, 3)
                if counts[idx_from] - shift_amount >= 5:
                    counts[idx_from] -= shift_amount
                    counts[idx_to] += shift_amount

    return counts


def generate_sales_data(run_hash: str) -> Dict[str, Tuple[List[SaleRecord], List[SalesItemRecord]]]:
    """
    Generate historical sales and sales items for all days in the configured range.
    Returns a dictionary keyed by month name (e.g., 'Jan', 'Feb'):
      { 'Jan': ([SaleRecord, ...], [SalesItemRecord, ...]), ... }
    """
    all_days = get_calendar_days(YEAR, START_MONTH, END_MONTH)
    daily_counts = distribute_counts_across_days(TOTAL_RECORDS, len(all_days))

    # Fuel selection weights: Diesel and Regular 87 are most common at truckstops
    fuel_skus = list(FUEL_CONFIG.keys())
    fuel_weights = [0.45 if sku == "87" else (0.40 if sku == "Diesel" else 0.15) for sku in fuel_skus]

    primary_location = LOCATIONS[0] if LOCATIONS else "1"

    monthly_data: Dict[str, Tuple[List[SaleRecord], List[SalesItemRecord]]] = {}
    global_seq = 1

    for day_idx, current_day in enumerate(all_days):
        month_name = MONTH_REV_MAP[current_day.month]
        if month_name not in monthly_data:
            monthly_data[month_name] = ([], [])

        day_sales, day_items = monthly_data[month_name]
        records_today = daily_counts[day_idx]

        for _ in range(records_today):
            # Pick random second within the 24-hour day (0 to 86399)
            second_of_day = random.randint(0, 86399)
            sale_hour = second_of_day // 3600
            sale_minute = (second_of_day % 3600) // 60
            sale_second = second_of_day % 60
            sale_time_str = f"{sale_hour:02d}:{sale_minute:02d}:{sale_second:02d}"

            # Shift calculation: 0-5 -> 1, 6-11 -> 2, 12-17 -> 3, 18-23 -> 4
            shift_number = (sale_hour // 6) + 1

            # Select terminal and fuel product
            terminal = random.choice(TERMINALS)
            sku = random.choices(fuel_skus, weights=fuel_weights, k=1)[0]
            fuel_info = FUEL_CONFIG[sku]

            # Calculate gallons and total amount
            gallons = round(random.uniform(fuel_info["min_gallons"], fuel_info["max_gallons"]), 2)
            unit_price = fuel_info["unit_price"]
            total_amount = round(gallons * unit_price, 2)

            # Generate collision-free UUIDs
            sale_id = generate_sale_id(
                sim_date=current_day,
                location=primary_location,
                run_hash=run_hash,
                shift=shift_number,
                sequence=global_seq,
            )

            item_id = generate_item_id(
                sim_date=current_day,
                location=primary_location,
                run_hash=run_hash,
                sequence=global_seq,
                item_index=1,
            )

            sale = SaleRecord(
                sales_id=sale_id,
                sales_amount=total_amount,
                sales_date=current_day.strftime("%Y-%m-%d"),
                sales_time=sale_time_str,
                shift_number=shift_number,
                terminal=terminal,
            )

            item = SalesItemRecord(
                id=item_id,
                item_name=fuel_info["item_name"],
                quantity=gallons,
                sales_type=fuel_info["sales_type"],
                sku_code=sku,
                unit_price=unit_price,
                sales_id=sale_id,
            )

            day_sales.append(sale)
            day_items.append(item)
            global_seq += 1

    # Sort each month chronologically by sales_date and sales_time
    for month_name in monthly_data:
        sales_list, items_list = monthly_data[month_name]
        # Create a lookup from sale_id to sort key
        sort_keys = {s.sales_id: (s.sales_date, s.sales_time) for s in sales_list}
        sales_list.sort(key=lambda s: (s.sales_date, s.sales_time))
        items_list.sort(key=lambda item: sort_keys.get(item.sales_id, ("", "")))

    return monthly_data
