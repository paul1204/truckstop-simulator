# In-Memory Shift Report Generator

This module generates gas station shift reports entirely in memory and sends them to a Spring Boot REST API service. **No files are written to disk** - all data exists only during program execution.

## Features

- **In-Memory Only**: All shift reports are generated and processed in memory
- **No File I/O**: No files are written to or read from disk
- **API Integration**: Direct integration with Spring Boot REST API
- **Two Data Sources**: 
  - Dynamic generation with realistic business logic
  - Static pre-defined data for testing
- **Unique Shift Numbering**: Each shift gets a globally unique identifier

## Files

- `main.py` - Main entry point with interactive menu
- `shift_generator.py` - Dynamic shift report generation with business logic
- `generate_shifts.py` - Static shift data (converted to in-memory)
- `api_integration_example.py` - Spring Boot API integration

## Usage

### Quick Start
```bash
cd app/shift
python main.py
```

### Programmatic Usage

```python
from api_integration_example import ShiftReportAPI
from shift_generator import get_single_shift_report

# Initialize API client
api = ShiftReportAPI()

# Generate and send a single shift report
shift_report = get_single_shift_report("2024-04-01", 1, 1)
result = api.send_shift_report(shift_report)

# Generate and send weekly reports
results = api.send_weekly_reports("2024-04-01", 7)
```

## API Endpoint

The system sends data to:
```
POST http://localhost:8080/api/shiftProcessing/postShift
```

With multipart form data containing:
- `shift_report`: Text file with shift data
- `inventory_report`: Text file with inventory data (placeholder)

## Data Structure

Each shift report contains:
- **Basic Info**: Date, shift number, employee ID, manager ID
- **Fuel Sales**: Diesel, Regular, Mid-grade, Premium gasoline
- **Convenience Store**: Coffee, Sodas, Water, Beer, Medication
- **Restaurant**: Breakfast, Lunch, Dinner meals
- **Tobacco**: Cigarettes
- **Notes**: Shift-specific observations

## Shift Types

1. **Morning** (Shift 1): High coffee/breakfast sales
2. **Midday** (Shift 2): Peak lunch sales
3. **Evening** (Shift 3): High dinner/beer sales
4. **Late Night** (Shift 4): Reduced activity

## Weekend Multipliers

- Friday: 1.3x
- Saturday: 1.5x
- Sunday: 1.4x
- Weekdays: 1.0x

## Memory Management

All data is generated and processed in memory:
- No temporary files created
- No disk I/O operations
- Data exists only during program execution
- Automatic cleanup when program ends

## Error Handling

- Comprehensive API response handling
- Network error recovery
- Detailed logging of success/failure rates
- Graceful handling of missing data

## Testing

The system provides both static and dynamic data generation for testing:
- **Static**: Pre-defined data for consistent testing
- **Dynamic**: Realistic data with random variation for simulation
