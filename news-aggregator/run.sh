#!/bin/bash

# Start the scheduler in the background
echo "Starting scheduler..."
python scheduler.py &
SCHEDULER_PID=$!

# Start the Flask app
echo "Starting web server..."
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app &
WEB_PID=$!

# Function to handle shutdown
shutdown() {
    echo "Shutting down..."
    kill $SCHEDULER_PID
    kill $WEB_PID
    exit 0
}

# Trap SIGTERM and SIGINT
trap shutdown SIGTERM SIGINT

# Wait for processes
wait
