from config import SHIFT_SIMULATION_CONFIG, TOTAL_EMPLOYEES, MANAGER_IDS
from shift_generator import get_single_shift_report
from api_integration_example import ShiftReportAPI
from datetime import datetime, timedelta
import time

def simulate_shifts():
    """Simulate shift reports at regular intervals"""
    api = ShiftReportAPI()
    NUM_REQUESTS = SHIFT_SIMULATION_CONFIG["NUM_REQUESTS"]
    INTERVAL_SECONDS = SHIFT_SIMULATION_CONFIG["INTERVAL_SECONDS"]
    
    # Start from today at 12 AM
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    current_shift = 1
    current_employee = 1
    
    print(f"Starting shift simulation...")
    print(f"Total requests: {NUM_REQUESTS}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print(f"Starting date: {current_date.strftime('%Y-%m-%d')}")
    print(f"Starting shift: {current_shift}")
    print("-" * 50)
    
    for i in range(NUM_REQUESTS):
        try:
            date_str = current_date.strftime('%Y-%m-%d')
            shift_report = get_single_shift_report(
                date=date_str,
                daily_shift=current_shift,
                employee_id=current_employee
            )
            
            print(f"Request {i+1}/{NUM_REQUESTS}: Generating shift {current_shift} for {date_str} (Employee: {current_employee})")
            print(f"  Shift Number: {shift_report['shift_number']}")
            print(f"  Daily Shift: {shift_report['daily_shift']}")
            
            result = api.send_shift_report(shift_report)
            
            if result['success']:
                print(f"  ✓ Success: Status {result['status_code']}")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")

            current_shift += 1
            current_employee += 1
            
            
            if current_shift > 4:
                current_shift = 1
                current_date += timedelta(days=1)
                print(f"  → Moving to next day: {current_date.strftime('%Y-%m-%d')}")
            
            if current_employee > TOTAL_EMPLOYEES:
                current_employee = 1
                
        except Exception as e:
            print(f"Error occurred: {e}")
            
        time.sleep(INTERVAL_SECONDS)
    
    print("-" * 50)
    print("Shift simulation completed!")
    print(f"Final date: {current_date.strftime('%Y-%m-%d')}")
    print(f"Final shift: {current_shift}")
    print(f"Final employee: {current_employee}")

if __name__ == "__main__":
    simulate_shifts()
