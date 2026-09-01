#!/usr/bin/env python3
from __future__ import annotations

import time, random
from datetime import datetime
from typing import List, Dict

import requests

from .config import API_URL, INTERVAL_SECONDS, DEFAULT_RESERVATION_DURATION
from app.time_management.time_manager import get_simulated_time

# Hard-coded array of spotNumbers from "A1" to "A10"
SPOT_NUMBERS: List[str] = [f"A{i:02}" for i in range(1, 11)]

RATE_TYPE = "HOURLY"

def _format_dt(dt: datetime) -> str:
    return dt.isoformat()

def build_payload(spot_number: str) -> Dict[str, str]:
    now = get_simulated_time()
    end_time = now + DEFAULT_RESERVATION_DURATION
    return {
        "spotNumber": spot_number,
        "vehicleRegistration": f"VA {random.randint(10000, 99999)}",
        "rateType": RATE_TYPE,
        "startTime": _format_dt(now),
        "endTime": _format_dt(end_time),
    }

def send_reservation(spot_number: str) -> Dict[str, object]:
    payload = build_payload(spot_number)
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        ok = response.status_code in (200, 201, 202)
        return {
            "spot": spot_number,
            "success": ok,
            "status_code": response.status_code,
            "response": (response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text),
        }
    except requests.exceptions.RequestException as e:
        return {"spot": spot_number, "success": False, "error": str(e)}


def reserve_all_spots() -> List[str]:
    messages: List[str] = []

    print(f"Target endpoint (POST): {API_URL}")
    print(f"Spots to reserve: {', '.join(SPOT_NUMBERS)}")
    print(f"Interval between requests: {INTERVAL_SECONDS} seconds\n")

    total = len(SPOT_NUMBERS)
    for idx, spot in enumerate(SPOT_NUMBERS, start=1):
        result = send_reservation(spot)
        if result.get("success"):
            status = result.get("status_code")
            print({spot})
            messages.append(f"Spot {spot}: success (status {status})")
        else:
            err = result.get("error") or f"status {result.get('status_code')}: {result.get('response')}"
            print({spot})
            messages.append(f"Spot {spot}: failed - {err}")

        if idx < total:
            time.sleep(INTERVAL_SECONDS)

    return messages