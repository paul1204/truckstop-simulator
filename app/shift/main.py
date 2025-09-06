from api_integration_example import ShiftReportAPI
#from shift_generator import get_shift_reports_for_api, get_single_shift_report, get_monthly_shift_reports_for_api
from config import MONTHS, DEFAULT_YEAR, MIN_YEAR, MAX_YEAR, TOTAL_EMPLOYEES, TOTAL_MANAGERS, SHIFTS_PER_DAY
import json

def display_months():
    """Display available months for selection"""
    print("\nAvailable months:")
    for key, name in MONTHS.items():
        print(f"  {key} - {name}")

def get_month_selection():
    """Get month selection from user"""
    while True:
        try:
            display_months()
            choice = input(f"\nEnter month code (e.g., 'JAN'): ").strip().upper()
            
            # Check if it's a valid month code
            if choice in MONTHS:
                return choice, MONTHS[choice]
            else:
                print("Invalid month code. Please try again.")
                continue
                
        except (ValueError, KeyboardInterrupt):
            print("\nInvalid input. Please try again.")
            continue

def get_year_selection():
    """Get year selection from user"""
    while True:
        try:
            year_input = input(f"\nEnter year ({MIN_YEAR}-{MAX_YEAR}) [default: {DEFAULT_YEAR}]: ").strip()
            
            if not year_input:
                return DEFAULT_YEAR
            
            year = int(year_input)
            if MIN_YEAR <= year <= MAX_YEAR:
                return year
            else:
                print(f"Please enter a year between {MIN_YEAR} and {MAX_YEAR}")
                continue
                
        except (ValueError, KeyboardInterrupt):
            print("Invalid input. Please try again.")
            continue

def get_month_number(month_key):
    """Convert month key to month number"""
    month_keys = list(MONTHS.keys())
    return month_keys.index(month_key) + 1

def show_main_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("=== Gas Station Shift Report Generator (In-Memory Only) ===")
    print("="*60)
    print(f"Configuration:")
    print(f"  Total Employees: {TOTAL_EMPLOYEES}")
    print(f"  Total Managers: {TOTAL_MANAGERS}")
    print(f"  Shifts per Day: {SHIFTS_PER_DAY}")
    
    print("\nChoose an option:")
    print("1. Generate and send single shift report")
    print("2. Generate and send monthly reports")
    print("3. Generate and send yearly reports")
    print("4. Generate reports in memory only (no API call)")
    print("5. Exit")

def main():
    """Main function to demonstrate in-memory shift report generation and API integration"""
    while True:
        try:
            show_main_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
        
            if choice == "1":
                print("\n--- Single Shift Report ---")
                
                # Get month and year
                month_key, month_name = get_month_selection()
                year = get_year_selection()
                month_num = get_month_number(month_key)
                
                # Get specific date and shift
                while True:
                    try:
                        day = int(input(f"\nEnter day of month (1-31): "))
                        if 1 <= day <= 31:
                            break
                        else:
                            print("Please enter a valid day (1-31)")
                    except ValueError:
                        print("Please enter a valid number")
                
                while True:
                    try:
                        daily_shift = int(input(f"Enter shift number (1-{SHIFTS_PER_DAY}): "))
                        if 1 <= daily_shift <= SHIFTS_PER_DAY:
                            break
                        else:
                            print(f"Please enter a shift number between 1 and {SHIFTS_PER_DAY}")
                    except ValueError:
                        print("Please enter a valid number")
                
                while True:
                    try:
                        employee_id = int(input(f"Enter employee ID (1-{TOTAL_EMPLOYEES}): "))
                        if 1 <= employee_id <= TOTAL_EMPLOYEES:
                            break
                        else:
                            print(f"Please enter an employee ID between 1 and {TOTAL_EMPLOYEES}")
                    except ValueError:
                        print("Please enter a valid number")
                
                # Generate date string
                date_str = f"{year}-{month_num:02d}-{day:02d}"
                
                # Generate shift report
                shift_report = get_single_shift_report(date_str, daily_shift, employee_id)
                print(f"\nGenerated shift report for {month_name} {day}, {year}:")
                print(json.dumps(shift_report, indent=2))
                
                # Send to API
                api = ShiftReportAPI()
                print(f"\nSending to API...")
                result = api.send_shift_report(shift_report)
                print(f"\nAPI Response Summary:")
                print(f"  Success: {result['success']}")
                print(f"  Status Code: {result['status_code']}")
                if 'response' in result and result['response']:
                    print(f"  Response Data: {result['response']}")
                if 'error' in result and result['error']:
                    print(f"  Error: {result['error']}")
                if 'raw_text' in result and result['raw_text']:
                    print(f"  Raw Response: {result['raw_text']}")
                
                input("\nPress Enter to return to main menu...")
                
            elif choice == "2":
                print("\n--- Monthly Reports ---")
                
                # Get month and year
                month_key, month_name = get_month_selection()
                year = get_year_selection()
                month_num = get_month_number(month_key)
                
                # Generate and send monthly reports
                api = ShiftReportAPI()
                print(f"\nGenerating and sending monthly reports for {month_name} {year}...")
                results = api.send_monthly_reports(year, month_num)
                
                print(f"\nResults:")
                print(f"Total shifts: {results['total_shifts']}")
                print(f"Successful: {results['successful_shifts']}")
                print(f"Failed: {results['failed_shifts']}")
                
                input("\nPress Enter to return to main menu...")
                
            elif choice == "3":
                print("\n--- Yearly Reports ---")
                
                # Get year
                year = get_year_selection()
                
                # Generate and send yearly reports
                api = ShiftReportAPI()
                print(f"\nGenerating and sending yearly reports for {year}...")
                print("This will process all 12 months...")
                
                yearly_results = {
                    'total_shifts': 0,
                    'successful_shifts': 0,
                    'failed_shifts': 0,
                    'monthly_breakdown': {}
                }
                
                # Process each month
                for month_num in range(1, 13):
                    month_name = list(MONTHS.values())[month_num - 1]
                    print(f"\nProcessing {month_name} {year}...")
                    
                    # Generate and send monthly reports
                    monthly_results = api.send_monthly_reports(year, month_num)
                    
                    # Aggregate results
                    yearly_results['total_shifts'] += monthly_results['total_shifts']
                    yearly_results['successful_shifts'] += monthly_results['successful_shifts']
                    yearly_results['failed_shifts'] += monthly_results['failed_shifts']
                    yearly_results['monthly_breakdown'][month_name] = {
                        'total': monthly_results['total_shifts'],
                        'successful': monthly_results['successful_shifts'],
                        'failed': monthly_results['failed_shifts']
                    }
                
                print(f"\n=== Yearly Results for {year} ===")
                print(f"Total shifts: {yearly_results['total_shifts']}")
                print(f"Successful: {yearly_results['successful_shifts']}")
                print(f"Failed: {yearly_results['failed_shifts']}")
                
                print(f"\nMonthly Breakdown:")
                for month, stats in yearly_results['monthly_breakdown'].items():
                    print(f"  {month}: {stats['successful']}/{stats['total']} successful")
                
                input("\nPress Enter to return to main menu...")
                
            elif choice == "4":
                print("\n--- Memory-Only Generation ---")
                
                # Get month and year
                month_key, month_name = get_month_selection()
                year = get_year_selection()
                month_num = get_month_number(month_key)
                
                print(f"\nGenerating reports in memory for {month_name} {year} (no API calls)...")
                
                # Generate monthly data
                monthly_reports = get_monthly_shift_reports_for_api(year, month_num)
                total_shifts = sum(len(shifts) for shifts in monthly_reports.values())
                print(f"Generated {total_shifts} shift reports for {len(monthly_reports)} days")
                
                # Show sample data
                first_day = list(monthly_reports.keys())[0]
                sample_shift = monthly_reports[first_day][0]
                
                print(f"\nSample Report for {first_day}:")
                print(f"  Daily Shift: {sample_shift['daily_shift']}")
                print(f"  Unique Shift Number: {sample_shift['shift_number']}")
                print(f"  Employee: {sample_shift['employee_id']}")
                print(f"  Manager: {sample_shift['manager_id']}")
                print(f"  Fuel Sales: {sample_shift['fuel_sales']['total_gasoline_sales']}")
                print(f"  Convenience Sales: {sample_shift['convenience_store_sales']['total_convenience_store_sales']}")
                print(f"  Restaurant Sales: {sample_shift['restaurant_sales']['total_restaurant_sales']}")
                print(f"  Tobacco Sales: {sample_shift['tobacco_sales']['total_tobacco_sales']}")
                
                input("\nPress Enter to return to main menu...")
                
            elif choice == "5":
                print("\n=== Exiting Gas Station Shift Report Generator ===")
                print("Thank you for using the system!")
                break
                
            else:
                print("Invalid choice. Please select 1-5.")
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to continue...")
    
    print("\n=== All operations completed in memory only - no files written to disk ===")

if __name__ == "__main__":
    main()