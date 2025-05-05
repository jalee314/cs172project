@echo off
REM Usage: crawler.bat [num_threads] [max_file_size_mb]

set THREADS=10
set MAX_SIZE_MB=10

REM Override if arguments are passed
if not "%~1"=="" set THREADS=%~1
if not "%~2"=="" set MAX_SIZE_MB=%~2

echo Starting Reddit crawler with %THREADS% threads and max file size of %MAX_SIZE_MB% MB...

python3 crawler.py --threads %THREADS% --max-size-mb %MAX_SIZE_MB%

pause