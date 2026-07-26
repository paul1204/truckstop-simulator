#!/usr/bin/env python3

import requests
import json
from io import BytesIO
from shift_generator import get_shift_reports_for_api, get_single_shift_report, get_monthly_shift_reports_for_api

class ShiftReportAPI:
    """Example integration with Spring Boot REST API"""
    
    def __init__(self, base_url: str = "http://localhost:9000/api/shiftProcessing"):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/postShift"
    
    def create_multipart_data(self, shift_report: dict) -> tuple:
        """Convert shift report to multipart form data"""
        # Convert shift report to text format
        shift_text = self._format_shift_report_text(shift_report)
        
        # Create file-like objects for multipart data
        shift_file = BytesIO(shift_text.encode('utf-8'))
        inventory_file = BytesIO(b"INVENTORY_REPORT_PLACEHOLDER")  # You can customize this
        
        return shift_file, inventory_file
    
    def send_shift_report(self, shift_report: dict) -> dict:
        """Send a single shift report to the Spring Boot API"""
        try:
            shift_file, inventory_file = self.create_multipart_data(shift_report)
            
            files = {
                'shift_report': ('shift_report.txt', shift_file, 'text/plain'),
                'inventory_report': ('inventory_report.txt', inventory_file, 'text/plain')
            }
            
          #  print(f"  Sending POST request to: {self.endpoint}")
            response = requests.post(self.endpoint, files=files)
          #  print(f"  Response Status Code: {response.status_code}")
          #  print(f"  Response Headers: {dict(response.headers)}")
          #  print(f"  Response Content: {response.text}")
          #  print(f"  Response Content Length: {len(response.content)}")
            
            # Check if response has content before trying to parse JSON
            response_json = None
            if response.content:
                try:
                    response_json = response.json()
                    #print(f"  Parsed JSON Response: {response_json}")
                except ValueError as e:
                    print(f"  JSON Parse Error: {e}")
                    print(f"  Raw Content: {response.text}")
            
            # Consider 200, 201, 202 as success
            if response.status_code in [200, 201, 202]:
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'response': response_json,
                    'raw_text': response.text
                }
            else:
                return {
                    'success': False,
                    'status_code': response.status_code,
                    'error': response.text,
                    'response': response_json
                }
                
        except requests.exceptions.RequestException as e:
            print(f"  Request Exception: {e}")
            return {
                'success': False,
                'error': f"Request failed: {str(e)}"
            }
    
    def send_weekly_reports(self, start_date: str = "2024-04-01", num_days: int = 7, use_static_data: bool = False) -> dict:
        """Send a week's worth of shift reports (in-memory only)"""
        # Generate all shift reports in memory
        if use_static_data:
            weekly_reports = get_static_shift_reports_for_api(start_date, num_days)
        else:
            weekly_reports = get_shift_reports_for_api(start_date, num_days)
        
        results = {
            'total_shifts': 0,
            'successful_shifts': 0,
            'failed_shifts': 0,
            'responses': []
        }
        
        # Send each shift report
        for date, shifts in weekly_reports.items():
            for shift in shifts:
                results['total_shifts'] += 1
                
                print(f"Sending shift {shift['daily_shift']} (Unique: {shift['shift_number']}) for {date}...")
                response = self.send_shift_report(shift)
                
                results['responses'].append({
                    'date': date,
                    'daily_shift': shift['daily_shift'],
                    'unique_shift_number': shift['shift_number'],
                    'employee_id': shift['employee_id'],
                    'response': response
                })
                
                if response['success']:
                    results['successful_shifts'] += 1
                else:
                    results['failed_shifts'] += 1
        
        return results
    
    def send_monthly_reports(self, year: int, month: int) -> dict:
        """Send a month's worth of shift reports (in-memory only)"""
        # Generate all shift reports in memory
        monthly_reports = get_monthly_shift_reports_for_api(year, month)
        
        results = {
            'total_shifts': 0,
            'successful_shifts': 0,
            'failed_shifts': 0,
            'responses': []
        }
        
        # Send each shift report
        for date, shifts in monthly_reports.items():
            for shift in shifts:
                results['total_shifts'] += 1
                
                print(f"Sending shift {shift['daily_shift']} (Unique: {shift['shift_number']}) for {date}...")
                response = self.send_shift_report(shift)
                
                results['responses'].append({
                    'date': date,
                    'daily_shift': shift['daily_shift'],
                    'unique_shift_number': shift['shift_number'],
                    'employee_id': shift['employee_id'],
                    'response': response
                })
                
                if response['success']:
                    results['successful_shifts'] += 1
                else:
                    results['failed_shifts'] += 1
        
        return results

    def _format_shift_report_text(self, shift_report: dict) -> str:
        """Format shift report as text for file upload"""
        text = f"""DATE: {shift_report['date']}
  SHIFT_NUMBER: {shift_report['shift_number']}
  DAILY_SHIFT: {shift_report['daily_shift']}
  EMPLOYEE_ID: {shift_report['employee_id']}
  MANAGER_ID: {shift_report['manager_id']}

  STARTING_DRAWER_POS1: {shift_report['starting_drawer_pos1']}
  STARTING_DRAWER_POS2: {shift_report['starting_drawer_pos2']}

  FUEL_SALES:
    DIESEL_TRANSACTIONS: {shift_report['fuel_sales']['diesel_transactions']}
    REGULAR_GASOLINE_TRANSACTIONS: {shift_report['fuel_sales']['regular_gasoline_transactions']}
    MID_GRADE_GASOLINE_TRANSACTIONS: {shift_report['fuel_sales']['mid_grade_gasoline_transactions']}
    PREMIUM_GASOLINE_TRANSACTIONS: {shift_report['fuel_sales']['premium_gasoline_transactions']}
    TOTAL_GASOLINE_SALES: {shift_report['fuel_sales']['total_gasoline_sales']}

  CONVENIENCE_STORE_SALES:
    COFFEE: {shift_report['convenience_store_sales']['coffee']}
    SODAS: {shift_report['convenience_store_sales']['sodas']}
    WATER_BOTTLES: {shift_report['convenience_store_sales']['water_bottles']}
    BEER: {shift_report['convenience_store_sales']['beer']}
    MEDICATION: {shift_report['convenience_store_sales']['medication']}
    TOTAL_CONVENIENCE_STORE_SALES: {shift_report['convenience_store_sales']['total_convenience_store_sales']}

  RESTAURANT_SALES:
    BREAKFAST_MEALS: {shift_report['restaurant_sales']['breakfast_meals']}
    LUNCH_MEALS: {shift_report['restaurant_sales']['lunch_meals']}
    DINNER_MEALS: {shift_report['restaurant_sales']['dinner_meals']}
    TOTAL_RESTAURANT_SALES: {shift_report['restaurant_sales']['total_restaurant_sales']}

  TOBACCO_SALES:
    CIGARETTES: {shift_report['tobacco_sales']['cigarettes']}
    TOTAL_TOBACCO_SALES: {shift_report['tobacco_sales']['total_tobacco_sales']}

    SHIFT_NOTES:
    """
        for note in shift_report['shift_notes']:
            text += f"  - {note}\n"
        
        return text
