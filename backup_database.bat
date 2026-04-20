@echo off
REM Database backup script for testplatform project
REM This script will create a backup of the MySQL database

echo Starting database backup...

REM Configuration
set DB_HOST=127.0.0.1
set DB_PORT=3311
set DB_NAME=testplatform
set DB_USER=root
set DB_PASSWORD=123456
set BACKUP_DIR=%~dp0backups
set DATESTAMP=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set DATESTAMP=%DATESTAMP: =0%

REM Create backups directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Create backup file name
set BACKUP_FILE=%BACKUP_DIR%\%DB_NAME%_backup_%DATESTAMP%.sql

REM Perform database backup
echo Backing up database to %BACKUP_FILE%
mysqldump -h %DB_HOST% -P %DB_PORT% -u %DB_USER% -p%DB_PASSWORD% %DB_NAME% > "%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo Database backup completed successfully!
    echo Backup file: %BACKUP_FILE%
) else (
    echo Error occurred during database backup!
    echo Please check your MySQL connection settings and ensure mysqldump is in your PATH.
)

pause