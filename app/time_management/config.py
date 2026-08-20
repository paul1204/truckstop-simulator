from datetime import datetime

# --- Time Management Configuration ---

# The duration of one simulated day in real-world minutes
REAL_MINUTES_PER_SIMULATED_DAY = 10.0

# The simulated starting date and time for the simulation run
# This starts dynamically at 12:00 AM (00:00:00) of today
START_SIMULATION_TIME = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
