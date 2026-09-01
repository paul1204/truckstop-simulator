FROM python:3.13-slim

# Force Python output directly to terminal (no buffering) so logs appear in real-time
ENV PYTHONUNBUFFERED=1

# Add both /app and /app/app to Python search path (matches PyCharm source roots)
ENV PYTHONPATH="/app:/app/app"

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the simulation module
CMD ["python", "-m", "simulate_truckstop_services"]
