#!/usr/bin/env python3

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import TOTAL_EMPLOYEES, MANAGER_IDS, SHIFTS_PER_DAY

class ShiftReportGenerator:
    """Generate realistic shift reports for gas station operations"""
    def __init__(self):
        # Base templates for different shift types
        self.shift_templates = {
            "morning": {
                "fuel_multiplier": 1.2,
                "coffee_multiplier": 1.5,
                "breakfast_multiplier": 1.4,
                "notes": [
                    "Busy morning rush for coffee and breakfast.",
                    "Steady fuel sales throughout shift.",
                    "High demand for water bottles due to warm weather.",
                    "Light dinner traffic as expected."
                ]
            },
            "midday": {
                "fuel_multiplier": 1.0,
                "soda_multiplier": 1.3,
                "lunch_multiplier": 1.6,
                "notes": [
                    "Peak lunch hour was very busy.",
                    "Good dinner sales in restaurant.",
                    "Moderate fuel activity.",
                    "Tobacco sales steady."
                ]
            },
            "evening": {
                "fuel_multiplier": 0.8,
                "beer_multiplier": 1.4,
                "dinner_multiplier": 1.5,
                "notes": [
                    "Evening dinner rush was excellent.",
                    "Beer sales increased in evening hours.",
                    "Lower fuel volume as expected for evening.",
                    "Restaurant had strong dinner performance."
                ]
            },
            "late_night": {
                "fuel_multiplier": 0.5,
                "beer_multiplier": 1.2,
                "dinner_multiplier": 0.6,
                "notes": [
                    "Late night shift with reduced activity.",
                    "Beer sales remained steady.",
                    "Minimal fuel transactions.",
                    "Quiet restaurant service."
                ]
            }
        }
        
        # Base sales data
        self.base_sales = {
            "fuel": {
                "diesel": 30,
                "regular": 100,
                "mid_grade": 30,
                "premium": 20
            },
            "convenience": {
                "coffee": 60,
                "sodas": 70,
                "water_bottles": 100,
                "beer": 25,
                "medication": 15
            },
            "restaurant": {
                "breakfast_meals": 80,
                "lunch_meals": 100,
                "dinner_meals": 80
            },
            "tobacco": {
                "cigarettes": 60
            }
        }
        
        # Weekend multipliers
        self.weekend_multipliers = {
            "friday": 1.3,
            "saturday": 1.5,
            "sunday": 1.4,
            "weekday": 1.0
        }
    
    def _get_shift_type(self, shift_number: int) -> str:
        """Determine shift type based on shift number (1-4 for each day)"""
        # Convert unique shift number to daily shift type (1-4)
        daily_shift = ((shift_number - 1) % 4) + 1
        
        if daily_shift == 1:
            return "morning"
        elif daily_shift == 2:
            return "midday"
        elif daily_shift == 3:
            return "evening"
        else:
            return "late_night"
    
    def _get_weekend_multiplier(self, date: datetime) -> float:
        """Get weekend multiplier based on date"""
        weekday = date.strftime("%A").lower()
        if weekday == "friday":
            return self.weekend_multipliers["friday"]
        elif weekday == "saturday":
            return self.weekend_multipliers["saturday"]
        elif weekday == "sunday":
            return self.weekend_multipliers["sunday"]
        else:
            return self.weekend_multipliers["weekday"]
    
    def _calculate_sales(self, base_value: int, shift_multiplier: float, 
                        weekend_multiplier: float, random_variation: float = 0.2) -> int:
        """Calculate sales with multipliers and random variation"""
        variation = random.uniform(1 - random_variation, 1 + random_variation)
        return int(base_value * shift_multiplier * weekend_multiplier * variation)
    
    def _calculate_total_sales(self, sales_dict: Dict[str, int], 
                              price_per_unit: Dict[str, float]) -> float:
        """Calculate total sales amount"""
        total = 0
        for item, quantity in sales_dict.items():
            if item in price_per_unit:
                total += quantity * price_per_unit[item]
        return total
    
    def _generate_unique_shift_number(self, date: str, daily_shift: int) -> int:
        """Generate unique shift number based on date and daily shift (1-4)"""
        # Convert date to days since epoch for unique calculation
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        days_since_epoch = (date_obj - datetime(1970, 1, 1)).days
        
        # Formula: (days_since_epoch * 4) + daily_shift
        # This ensures unique shift numbers across all days
        unique_shift_number = (days_since_epoch * 4) + daily_shift
        
        return unique_shift_number
    
    def generate_shift_report(self, date: str, daily_shift: int, 
                            employee_id: int, manager_id: int = None) -> Dict[str, Any]:
        """Generate a single shift report"""
        
        # Generate unique shift number
        unique_shift_number = self._generate_unique_shift_number(date, daily_shift)
        
        # Use default manager if none provided
        if manager_id is None:
            manager_id = MANAGER_IDS[0]  # Use first manager as default
        
        # Parse date
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        shift_type = self._get_shift_type(unique_shift_number)
        weekend_multiplier = self._get_weekend_multiplier(date_obj)
        template = self.shift_templates[shift_type]
        
        # Generate fuel sales
        fuel_sales = {}
        for fuel_type, base_value in self.base_sales["fuel"].items():
            fuel_sales[fuel_type] = self._calculate_sales(
                base_value, template.get("fuel_multiplier", 1.0), weekend_multiplier
            )
        
        # Generate convenience store sales
        convenience_sales = {}
        for item, base_value in self.base_sales["convenience"].items():
            multiplier = template.get(f"{item}_multiplier", 1.0)
            convenience_sales[item] = self._calculate_sales(
                base_value, multiplier, weekend_multiplier
            )
        
        # Generate restaurant sales
        restaurant_sales = {}
        for meal_type, base_value in self.base_sales["restaurant"].items():
            multiplier = template.get(f"{meal_type.split('_')[0]}_multiplier", 1.0)
            restaurant_sales[meal_type] = self._calculate_sales(
                base_value, multiplier, weekend_multiplier
            )
        
        # Generate tobacco sales
        tobacco_sales = {}
        for item, base_value in self.base_sales["tobacco"].items():
            tobacco_sales[item] = self._calculate_sales(
                base_value, 1.0, weekend_multiplier
            )
        
        # Calculate totals (using estimated prices)
        fuel_prices = {"diesel": 4.50, "regular": 3.80, "mid_grade": 4.10, "premium": 4.40}
        convenience_prices = {"coffee": 2.50, "sodas": 1.75, "water_bottles": 1.25, 
                            "beer": 3.50, "medication": 8.00}
        restaurant_prices = {"breakfast_meals": 12.00, "lunch_meals": 15.00, "dinner_meals": 18.00}
        tobacco_prices = {"cigarettes": 5.00}
        
        total_fuel_sales = self._calculate_total_sales(fuel_sales, fuel_prices)
        total_convenience_sales = self._calculate_total_sales(convenience_sales, convenience_prices)
        total_restaurant_sales = self._calculate_total_sales(restaurant_sales, restaurant_prices)
        total_tobacco_sales = self._calculate_total_sales(tobacco_sales, tobacco_prices)
        
        # Create shift report
        shift_report = {
            "date": date,
            "shift_number": unique_shift_number,  # Unique shift number (e.g., 73049)
            "daily_shift": daily_shift,  # Daily shift (1-4) for reference
            "employee_id": employee_id,
            "manager_id": manager_id,
            "starting_drawer_pos1": 100,
            "starting_drawer_pos2": 100,
            "fuel_sales": {
                "diesel_transactions": fuel_sales["diesel"],
                "regular_gasoline_transactions": fuel_sales["regular"],
                "mid_grade_gasoline_transactions": fuel_sales["mid_grade"],
                "premium_gasoline_transactions": fuel_sales["premium"],
                "total_gasoline_sales": f"${total_fuel_sales:,.2f}"
            },
            "convenience_store_sales": {
                "coffee": convenience_sales["coffee"],
                "sodas": convenience_sales["sodas"],
                "water_bottles": convenience_sales["water_bottles"],
                "beer": convenience_sales["beer"],
                "medication": convenience_sales["medication"],
                "total_convenience_store_sales": f"${total_convenience_sales:,.2f}"
            },
            "restaurant_sales": {
                "breakfast_meals": restaurant_sales["breakfast_meals"],
                "lunch_meals": restaurant_sales["lunch_meals"],
                "dinner_meals": restaurant_sales["dinner_meals"],
                "total_restaurant_sales": f"${total_restaurant_sales:,.2f}"
            },
            "tobacco_sales": {
                "cigarettes": tobacco_sales["cigarettes"],
                "total_tobacco_sales": f"${total_tobacco_sales:.2f}"
            },
            "shift_notes": template["notes"]
        }
        
        return shift_report
    
    def generate_daily_shifts(self, date: str, employee_ids: List[int] = None) -> List[Dict[str, Any]]:
        """Generate all shifts for a given date using config settings"""
        if employee_ids is None:
            # Generate employee IDs using config settings
            # Rotate through available employees
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            start_employee = ((date_obj - datetime(2024, 1, 1)).days * SHIFTS_PER_DAY) % TOTAL_EMPLOYEES + 1
            employee_ids = []
            for i in range(SHIFTS_PER_DAY):
                employee_id = ((start_employee + i - 1) % TOTAL_EMPLOYEES) + 1
                employee_ids.append(employee_id)
        
        shifts = []
        for daily_shift in range(1, SHIFTS_PER_DAY + 1):  # Use config setting
            shift_report = self.generate_shift_report(
                date, daily_shift, employee_ids[daily_shift - 1]
            )
            shifts.append(shift_report)
        
        return shifts
    
    def generate_weekly_shifts(self, start_date: str, num_days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """Generate shifts for multiple days"""
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        weekly_shifts = {}
        
        for day in range(num_days):
            current_date = start_date_obj + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            weekly_shifts[date_str] = self.generate_daily_shifts(date_str)
        
        return weekly_shifts
    
    def generate_monthly_shifts(self, year: int, month: int) -> Dict[str, List[Dict[str, Any]]]:
        """Generate shifts for an entire month"""
        # Get first day of the month
        start_date = datetime(year, month, 1)
        
        # Get last day of the month
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        
        last_day = (next_month - timedelta(days=1)).day
        
        monthly_shifts = {}
        
        for day in range(1, last_day + 1):
            current_date = datetime(year, month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            monthly_shifts[date_str] = self.generate_daily_shifts(date_str)
        
        return monthly_shifts
    
    def format_shift_report_text(self, shift_report: Dict[str, Any]) -> str:
        """Format shift report as text (for file output if needed)"""
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

# Example usage for REST API
def get_shift_reports_for_api(start_date: str = "2024-04-01", num_days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
    """Get shift reports formatted for REST API consumption"""
    generator = ShiftReportGenerator()
    return generator.generate_weekly_shifts(start_date, num_days)

def get_single_shift_report(date: str, daily_shift: int, employee_id: int) -> Dict[str, Any]:
    """Get a single shift report for API consumption"""
    generator = ShiftReportGenerator()
    return generator.generate_shift_report(date, daily_shift, employee_id)

def get_monthly_shift_reports_for_api(year: int, month: int) -> Dict[str, List[Dict[str, Any]]]:
    """Get monthly shift reports formatted for REST API consumption"""
    generator = ShiftReportGenerator()
    return generator.generate_monthly_shifts(year, month)

# Example usage
if __name__ == "__main__":
    # Example: Generate a week of shift reports
    weekly_reports = get_shift_reports_for_api("2024-04-01", 7)
    
    # Print first day's first shift as example
    first_day = list(weekly_reports.keys())[0]
    first_shift = weekly_reports[first_day][0]
    
    print("Example shift report:")
    print(f"Date: {first_shift['date']}")
    print(f"Unique Shift Number: {first_shift['shift_number']}")
    print(f"Daily Shift: {first_shift['daily_shift']}")
    print(f"Employee: {first_shift['employee_id']}")
    print(f"Total Fuel Sales: {first_shift['fuel_sales']['total_gasoline_sales']}")
    print(f"Total Convenience Sales: {first_shift['convenience_store_sales']['total_convenience_store_sales']}")
    print(f"Total Restaurant Sales: {first_shift['restaurant_sales']['total_restaurant_sales']}")
    print(f"Total Tobacco Sales: {first_shift['tobacco_sales']['total_tobacco_sales']}")
    
    # Print total number of shifts generated
    total_shifts = sum(len(shifts) for shifts in weekly_reports.values())
    print(f"\nGenerated {total_shifts} shift reports for {len(weekly_reports)} days")
    
    # Show unique shift numbers for first day
    print(f"\nFirst day ({first_day}) shift numbers:")
    for i, shift in enumerate(weekly_reports[first_day]):
        print(f"  Daily Shift {shift['daily_shift']}: Unique Shift Number {shift['shift_number']}") 