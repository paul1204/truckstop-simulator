# Truckstop Simulator

A Python simulator project for generating truckstop activity and sending test data to backend services.

The goal of this project is to make it easy to test truckstop service APIs with realistic sample activity across different areas of the business.

## What It Simulates

- Fuel sales
- Point-of-sale transactions
- Parking reservations
- Shift reports
- Restaurant delivery invoices

## Project Structure

app/
  fuel/
  parking_reservation/
  pointofsales/
  restaurant_delivery/
  shift/
  simulate_truckstop_services.py

requirements.txt
README.md

## Requirements

- Python 3.13+
- Virtual environment recommended
- Backend service running locally or at the configured API URLs

Install dependencies:

pip install -r requirements.txt

## Usage

Run the main simulator entry point when available.

Example:

python app/simulate_truckstop_services.py

Some modules include their own configuration files for API URLs, request timing, and simulation settings.

## Configuration

Configuration is handled inside each module through its `config.py` file when applicable.

Common configuration values may include:

- API endpoint URL
- Request interval
- Number of simulated requests
- Input data directory
- Form field names for file uploads