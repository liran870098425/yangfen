# Database Backup Instructions

This document explains how to backup the testplatform project database.

## Database Configuration

Based on the project configuration files, the database settings are:
- Type: MySQL
- Host: 127.0.0.1
- Port: 3311
- Database Name: testplatform
- Username: root
- Password: 123456

## Backup Methods

### Python-based Backup (No mysqldump required)

Since `mysqldump` is not available, a Python-based backup solution has been created:

- **[backup_database_python.py](file:///d:/django-testplatform_test/backup_database_python.py)** - Python script that connects directly to MySQL and exports data

To use this script:
1. Make sure you have Python installed
2. Install the required dependency: `pip install pymysql`
3. Run the script: `python backup_database_python.py`

This script will:
- Create a backup directory with timestamp
- Export each table as a separate JSON file with both structure and data
- Create a complete SQL backup file with table structures and data

### Manual Backup

You can also perform a manual backup using any MySQL client tool or GUI application that can export database structures and data.

## Restoring from Backup

### From JSON backups:
The JSON backup files contain both table structure and data. To restore:
1. Read the JSON file
2. Execute the `create_table_sql` to recreate the table structure
3. Insert the data from the `data` array

### From SQL backup:
The SQL backup file can be executed using any MySQL client:
```bash
mysql -h 127.0.0.1 -P 3311 -u root -p testplatform < backup_file.sql
```

## Prerequisites

- Python 3.x installed
- `pymysql` library installed (`pip install pymysql`)
- Network access to the database (port 3311 should be open)
- Database user must have sufficient privileges for backup operations

## Notes

- Backups are saved in the `backups` directory with timestamped folders
- Each backup folder contains both JSON files (one per table) and a complete SQL file
- Make sure to regularly backup your database, especially before major changes
- Store backups in a secure location separate from your server