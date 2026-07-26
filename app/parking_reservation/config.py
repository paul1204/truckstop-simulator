#!/usr/bin/env python3
from datetime import timedelta
from app.api_config import PARKING_RESERVE_URL as API_URL

# Seconds between sending each reservation request
INTERVAL_SECONDS = 1

DEFAULT_RESERVATION_DURATION = timedelta(hours=8)
