import os
import time
from datetime import datetime, timedelta
from .config import REAL_MINUTES_PER_SIMULATED_DAY, START_SIMULATION_TIME

START_FILE = os.path.join(os.path.dirname(__file__), "sim_start.tmp")

def reset_simulation_start():
    now = time.time()
    try:
        with open(START_FILE, "w") as f:
            f.write(str(now))
    except Exception as e:
        print(f"Error resetting simulation start file: {e}")
    return now

def get_real_start_time():
    now = time.time()
    if os.path.exists(START_FILE):
        try:
            with open(START_FILE, "r") as f:
                t = float(f.read().strip())
            # Keep active for up to 15 minutes of run time
            if now - t < 900.0:
                return t
        except Exception:
            pass
    return reset_simulation_start()

def cleanup_simulation_start():
    if os.path.exists(START_FILE):
        try:
            os.remove(START_FILE)
            print("Simulation start file cleaned up successfully.")
        except Exception:
            pass

# Calculate the speedup factor: 24 hours of simulated time / configured real minutes
SPEEDUP_FACTOR = 86400.0 / (REAL_MINUTES_PER_SIMULATED_DAY * 60.0)

def get_simulated_time():
    real_start = get_real_start_time()
    real_elapsed = time.time() - real_start
    simulated_elapsed_seconds = real_elapsed * SPEEDUP_FACTOR
    return START_SIMULATION_TIME + timedelta(seconds=simulated_elapsed_seconds)

def is_simulation_finished():
    real_start = get_real_start_time()
    real_elapsed = time.time() - real_start
    finished = real_elapsed >= (REAL_MINUTES_PER_SIMULATED_DAY * 60.0)
    if finished:
        cleanup_simulation_start()
    return finished

def get_simulated_shift(sim_time=None):
    if sim_time is None:
        sim_time = get_simulated_time()
    return (sim_time.hour // 6) + 1
