"""
SQL Writer for historical seed data.
Formats records into batched multi-row INSERT IGNORE INTO statements
and writes them in lockstep into the required directory hierarchy.
"""

import os
from typing import List, Tuple

from .config import (
    YEAR,
    BATCH_SIZE,
    SQL_INSERT_PREFIX,
    FILE_WRITE_MODE,
    OUTPUT_SQL_DIR,
)
from .models import SaleRecord, SalesItemRecord


def get_output_paths(month_name: str) -> Tuple[str, str]:
    """
    Return destination file paths for sales and sales_item SQL files.
    Format:
      sql/sales/<YEAR>/<Month>/<month_lower>_sales_<YEAR>.sql
      sql/sales_item/<YEAR>/<Month>/<month_lower>_sales_item_<YEAR>.sql
    """
    month_lower = month_name.lower()

    sales_dir = os.path.join(OUTPUT_SQL_DIR, "sales", str(YEAR), month_name)
    sales_item_dir = os.path.join(OUTPUT_SQL_DIR, "sales_item", str(YEAR), month_name)

    os.makedirs(sales_dir, exist_ok=True)
    os.makedirs(sales_item_dir, exist_ok=True)

    sales_file = os.path.join(sales_dir, f"{month_lower}_sales_{YEAR}.sql")
    sales_item_file = os.path.join(sales_item_dir, f"{month_lower}_sales_item_{YEAR}.sql")

    return sales_file, sales_item_file


def format_sales_batch(batch: List[SaleRecord], batch_num: int, start_idx: int) -> str:
    """Format a batch of SaleRecord into a batched SQL INSERT statement."""
    end_idx = start_idx + len(batch) - 1
    header = f"-- Batch {batch_num} (Rows {start_idx} to {end_idx})\n"
    insert_stmt = f"{SQL_INSERT_PREFIX} sales (sales_id, sales_amount, sales_date, sales_time, shift_number, terminal) VALUES\n"

    rows = []
    for s in batch:
        row_str = f"('{s.sales_id}', {s.sales_amount:.2f}, '{s.sales_date}', '{s.sales_time}', {s.shift_number}, '{s.terminal}')"
        rows.append(row_str)

    body = ",\n".join(rows) + ";\n\n"
    return header + insert_stmt + body


def format_items_batch(batch: List[SalesItemRecord], batch_num: int, start_idx: int) -> str:
    """Format a batch of SalesItemRecord into a batched SQL INSERT statement."""
    end_idx = start_idx + len(batch) - 1
    header = f"-- Batch {batch_num} (Rows {start_idx} to {end_idx})\n"
    insert_stmt = f"{SQL_INSERT_PREFIX} sales_items (id, item_name, quantity, sales_type, sku_code, unit_price, sales_id) VALUES\n"

    rows = []
    for item in batch:
        row_str = f"('{item.id}', '{item.item_name}', {item.quantity:.2f}, {item.sales_type}, '{item.sku_code}', {item.unit_price:.2f}, '{item.sales_id}')"
        rows.append(row_str)

    body = ",\n".join(rows) + ";\n\n"
    return header + insert_stmt + body


def write_month_sql(
    month_name: str,
    sales: List[SaleRecord],
    items: List[SalesItemRecord]
) -> Tuple[str, str, int, int]:
    """
    Write sales and sales_items for a month in lockstep batches.
    One batch written to sales.sql, immediately followed by the matching batch written to sales_item.sql.
    Returns (sales_file_path, items_file_path, sales_count, items_count).
    """
    sales_file, items_file = get_output_paths(month_name)

    mode = "w" if FILE_WRITE_MODE == "overwrite" else "a"

    # Open both files together to execute lockstep writes
    with open(sales_file, mode, encoding="utf-8") as f_sales, \
         open(items_file, mode, encoding="utf-8") as f_items:

        total_sales = len(sales)
        batch_num = 1

        for i in range(0, total_sales, BATCH_SIZE):
            sales_chunk = sales[i:i + BATCH_SIZE]
            items_chunk = items[i:i + BATCH_SIZE]

            # 1. Format and write sales batch
            sales_sql = format_sales_batch(sales_chunk, batch_num, i + 1)
            f_sales.write(sales_sql)
            f_sales.flush()

            # 2. Immediately format and write corresponding sales_items batch
            items_sql = format_items_batch(items_chunk, batch_num, i + 1)
            f_items.write(items_sql)
            f_items.flush()

            batch_num += 1

    return sales_file, items_file, len(sales), len(items)
