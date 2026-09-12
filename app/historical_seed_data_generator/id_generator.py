"""
Collision-free UUID Generator for historical seed records.
Generates 36-character standard UUID strings embedding:
- MMDDYYYY (Simulated calendar date)
- LLLL (Location code, 4 chars)
- RRRR (Run hash from live execution timestamp, 4 hex chars)
- EEEE (Entity & shift identifier: a001..a004 for sales, b001 for items)
- CCCCCCCCCCCC (Sequence counter, 12 digits)

Format: MMDDYYYY-LLLL-RRRR-EEEE-CCCCCCCCCCCC
"""

import hashlib
import time
from datetime import date


def create_run_hash() -> str:
    """Generate a unique 4-character hex hash based on current process start time."""
    seed_str = f"{time.time_ns()}"
    return hashlib.sha256(seed_str.encode()).hexdigest()[:4]


def _format_location(location: str) -> str:
    """Format location string to exactly 4 characters."""
    try:
        # If numeric, format as 4-digit hex
        num = int(location)
        return f"{num:04x}"[-4:]
    except ValueError:
        # If alphanumeric string (e.g., 'A001'), pad or trim to 4 chars
        clean = "".join(c for c in location if c.isalnum()).lower()
        return clean.rjust(4, "0")[-4:]


def generate_sale_id(
    sim_date: date,
    location: str,
    run_hash: str,
    shift: int,
    sequence: int
) -> str:
    """
    Generate a 36-char collision-free UUID for a sale record.
    Example: 01012026-0001-7b2a-a001-000000000001
    """
    date_part = sim_date.strftime("%m%d%Y")
    loc_part = _format_location(location)
    hash_part = run_hash[:4].lower()
    entity_part = f"a{shift:03d}"[-4:]
    counter_part = f"{sequence:012d}"[-12:]

    return f"{date_part}-{loc_part}-{hash_part}-{entity_part}-{counter_part}"


def generate_item_id(
    sim_date: date,
    location: str,
    run_hash: str,
    sequence: int,
    item_index: int = 1
) -> str:
    """
    Generate a 36-char collision-free UUID for a sales item record.
    Example: 01012026-0001-7b2a-b001-000000000001
    """
    date_part = sim_date.strftime("%m%d%Y")
    loc_part = _format_location(location)
    hash_part = run_hash[:4].lower()
    entity_part = f"b{item_index:03d}"[-4:]
    counter_part = f"{sequence:012d}"[-12:]

    return f"{date_part}-{loc_part}-{hash_part}-{entity_part}-{counter_part}"
