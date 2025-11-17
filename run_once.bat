@echo off
REM Chạy scraper 1 lần (không lặp lại)
REM Dùng file này với Windows Task Scheduler để chạy hàng ngày

cd /d "%~dp0"

echo ========================================
echo TrendForce Scraper - Run Once
echo ========================================
echo.

python -c "from scheduled_scraper import run_daily_scrape; run_daily_scrape()"

echo.
echo Done!
