#!/bin/bash

# Configuration
CONTAINER_NAME="postgres_db"
DB_NAME="devops_db"
DB_USER="postgres"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

echo "=== Starting Database Backup ==="

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# CyberSec check: Run pg_dump inside the running Docker container without exposing passwords
echo "Extracting database dump from container: $CONTAINER_NAME..."
docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

# Check if the backup file was successfully created and is not empty
if [ -s "$BACKUP_FILE" ]; then
    # Compress the backup file to save space
    gzip "$BACKUP_FILE"
    echo "SUCCESS: Backup completed successfully!"
    echo "Archive saved to: ${BACKUP_FILE}.gz"
else
    echo "ERROR: Backup failed or file is empty!"
    rm -f "$BACKUP_FILE"
    exit 1
fi

echo "=== Backup Process Finished ==="