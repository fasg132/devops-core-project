#!/bin/bash

# Configuration
URL="http://localhost"
LOG_FILE="./scripts/monitor.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "=== Running Health Check ==="

# Send a request to the website and get the HTTP status code
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$URL")

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "[$TIMESTAMP] SUCCESS: Website is healthy (HTTP 200)" >> "$LOG_FILE"
    echo "Website is UP and running."
else
    echo "[$TIMESTAMP] ALERT: Website is DOWN with Status Code: $HTTP_STATUS" >> "$LOG_FILE"
    echo "Website is DOWN! Attempting automatic recovery..."
    
    # Try to restart the docker containers
    docker-compose restart gateway web
    
    if [ $? -eq 0 ]; then
        echo "[$TIMESTAMP] RECOVERY: Containers restarted successfully." >> "$LOG_FILE"
        echo "Recovery successful."
    else
        echo "[$TIMESTAMP] CRITICAL: Automatic recovery failed!" >> "$LOG_FILE"
        echo "Recovery failed. Manual intervention required."
    fi
fi

echo "=== Health Check Finished ==="