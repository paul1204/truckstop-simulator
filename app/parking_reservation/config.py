#!/usr/bin/env python3
from datetime import timedelta
API_URL = "http://localhost:8080/api/parking/reserve"

# Seconds between sending each reservation request
INTERVAL_SECONDS = 1

DEFAULT_RESERVATION_DURATION = timedelta(hours=8)
