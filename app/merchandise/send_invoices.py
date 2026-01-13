#!/usr/bin/env python3
import time
from pathlib import Path
import requests
from typing import List

from .config import API_URL, FORM_FIELD_NAME, DELIVERY_INVOICE_DIR, INTERVAL_SECONDS


def find_csv_files(directory: Path) -> List[Path]:
    return [p for p in directory.glob("*.csv") if p.is_file()]


def send_csv_file(file_path: Path) -> dict:
    try:
        with file_path.open("rb") as f:
            files = {
                FORM_FIELD_NAME: (file_path.name, f, "text/csv")
            }
            response = requests.put(API_URL, files=files, timeout=30)

        result = {
            "success": response.status_code in (200, 201, 202, 204),
            "status_code": response.status_code,
            "text": response.text,
        }
        if not result["success"]:
            result["error"] = response.text
        return result
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


def send_all_invoices():
    csv_files = find_csv_files(DELIVERY_INVOICE_DIR)

    if not csv_files:
        print(f"No CSV files found in {DELIVERY_INVOICE_DIR}")
        return

    total = len(csv_files)
    print(f"Found {total} CSV file(s) in {DELIVERY_INVOICE_DIR}")
    print(f"Target endpoint (PUT): {API_URL}")
    print(f"Form field name: {FORM_FIELD_NAME}")
    print(f"Interval between requests: {INTERVAL_SECONDS} seconds\n")

    for idx, csv_path in enumerate(csv_files, start=1):
        print(f"[{idx}/{total}] Sending: {csv_path.name}")
        result = send_csv_file(csv_path)
        if result.get("success"):
            print(f"  ✓ Success (status {result.get('status_code')})")
        else:
            print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
        
        # Sleep between requests except after the last one
        if idx < total:
            time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    send_all_invoices()
