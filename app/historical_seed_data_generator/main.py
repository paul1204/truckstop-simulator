"""
Main entry point for the Historical Seed Data Generator.
Coordinates single-threaded data generation, SQL formatting, and file writing.
Includes benchmarking metrics and placeholder comments for future concurrency testing.
"""

import os
import sys
import time

# Ensure project root is in sys.path when running script directly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.historical_seed_data_generator.config import (
    START_MONTH,
    END_MONTH,
    YEAR,
    TOTAL_RECORDS,
    BATCH_SIZE,
    SQL_INSERT_PREFIX,
    FILE_WRITE_MODE,
    LOCATIONS,
    TERMINALS,
    OUTPUT_SQL_DIR,
)
from app.historical_seed_data_generator.id_generator import create_run_hash
from app.historical_seed_data_generator.generators import generate_sales_data
from app.historical_seed_data_generator.sql_writer import write_month_sql


# ==============================================================================
# CONCURRENCY BENCHMARKING PLACEHOLDERS (For future implementation)
# ==============================================================================
# Currently, this generator runs in a clean, single-threaded mode.
# When ready to benchmark against multi-threading and multi-processing:
#
# 1. Multi-Threading (ThreadPoolExecutor):
#    - Note: Bound by Python's Global Interpreter Lock (GIL) for CPU-heavy string formatting.
#    - Useful for measuring GIL overhead and I/O concurrency when writing files.
#    - Example hook:
#        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#            futures = [executor.submit(write_month_sql, m, s, i) for m, (s, i) in monthly_data.items()]
#
# 2. Multi-Processing (ProcessPoolExecutor):
#    - Bypasses GIL by distributing data generation and SQL formatting across CPU cores.
#    - Ideal for parallelizing record generation when scaling to 50k - 100k+ records.
#    - Example hook:
#        with concurrent.futures.ProcessPoolExecutor() as executor:
#            results = list(executor.map(generate_and_write_chunk, month_configs))
# ==============================================================================


def run_generator():
    """Execute historical seed data generation in single-threaded mode."""
    start_time = time.time()
    run_hash = create_run_hash()

    print("=" * 65)
    print("       TRUCKSTOP HISTORICAL SEED DATA GENERATOR")
    print("=" * 65)
    print(f"  Range          : {START_MONTH} to {END_MONTH} {YEAR}")
    print(f"  Target Sales   : {TOTAL_RECORDS:,} records (Daily grain)")
    print(f"  Batch Size     : {BATCH_SIZE} rows per INSERT statement")
    print(f"  Insert Prefix  : {SQL_INSERT_PREFIX}")
    print(f"  Write Mode     : {FILE_WRITE_MODE}")
    print(f"  Locations      : {LOCATIONS}")
    print(f"  Terminals      : {TERMINALS}")
    print(f"  Run Hash       : {run_hash} (Ensures collision-free IDs across runs)")
    print(f"  Execution Mode : Single-Threaded")
    print("-" * 65)

    # Step 1: Generate records across all calendar days
    gen_start = time.time()
    print(">> Generating sales and sales item records across daily calendar...")
    monthly_data = generate_sales_data(run_hash)
    gen_duration = time.time() - gen_start
    print(f"   Generated records in {gen_duration:.3f}s.")

    # Step 2: Write SQL files per month in lockstep
    print(">> Writing batched SQL files (sales and sales_item in lockstep)...")
    write_start = time.time()

    total_sales_written = 0
    total_items_written = 0
    written_files = []

    for month_name, (sales, items) in monthly_data.items():
        if not sales:
            continue
        s_file, i_file, s_cnt, i_cnt = write_month_sql(month_name, sales, items)
        total_sales_written += s_cnt
        total_items_written += i_cnt
        written_files.append((month_name, s_file, i_file, s_cnt, i_cnt))

    write_duration = time.time() - write_start
    total_elapsed = time.time() - start_time
    records_per_sec = total_sales_written / total_elapsed if total_elapsed > 0 else 0

    # Step 3: Print summary report
    print("-" * 65)
    print("GENERATED SQL FILES SUMMARY:")
    for month_name, s_file, i_file, s_cnt, i_cnt in written_files:
        print(f"  [{month_name}] Sales: {s_cnt:>4} rows -> {s_file}")
        print(f"         Items: {i_cnt:>4} rows -> {i_file}")

    print("-" * 65)
    print("PERFORMANCE METRICS:")
    print(f"  Total Sales Records : {total_sales_written:,}")
    print(f"  Total Item Records  : {total_items_written:,}")
    print(f"  Data Generation Time: {gen_duration:.3f}s")
    print(f"  SQL Disk Write Time : {write_duration:.3f}s")
    print(f"  Total Elapsed Time  : {total_elapsed:.3f}s")
    print(f"  Throughput          : {records_per_sec:,.1f} sales/sec")
    print("=" * 65)
    print("Done! SQL seed files are ready for backend import.")


if __name__ == "__main__":
    run_generator()
