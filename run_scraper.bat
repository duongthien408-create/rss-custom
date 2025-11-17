@echo off
REM Windows Batch file để chạy scraper
REM Có thể dùng với Task Scheduler

cd /d "%~dp0"
python scheduled_scraper.py

REM Nếu muốn chạy 1 lần rồi thoát, dùng file này
REM python -c "from scheduled_scraper import run_daily_scrape; run_daily_scrape()"

pause
