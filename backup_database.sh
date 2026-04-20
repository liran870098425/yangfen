#!/bin/bash
# Database backup script for testplatform project
# This script will create a backup of the MySQL database

echo "Starting database backup..."

# Configuration
DB_HOST="127.0.0.1"
DB_PORT="3311"
DB_NAME="testplatform"
DB_USER="root"
DB_PASSWORD="123456"
BACKUP_DIR="$(dirname "$0")/backups"
DATESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backups directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup file name
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_${DATESTAMP}.sql"

# Perform database backup
echo "Backing up database to $BACKUP_FILE"
mysqldump -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD $DB_NAME > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Database backup completed successfully!"
    echo "Backup file: $BACKUP_FILE"
else
    echo "Error occurred during database backup!"
    echo "Please check your MySQL connection settings and ensure mysqldump is in your PATH."
fi