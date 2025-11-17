"""
Script để chạy scraper theo lịch tự động
Sử dụng thư viện schedule để chạy hàng ngày
"""

import schedule
import time
from datetime import datetime
from trendforce_scraper import TrendForceScraper


def run_daily_scrape():
    """Hàm chạy scrape hàng ngày"""
    print(f"\n{'='*60}")
    print(f"Bắt đầu scrape lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    scraper = TrendForceScraper()

    try:
        # Scrape 3 trang đầu tiên
        articles = scraper.scrape_multiple_pages(
            start_page=1,
            end_page=3,
            delay=1.5
        )

        # Tạo tên file với timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        json_filename = f'trendforce_daily_{timestamp}.json'
        csv_filename = f'trendforce_daily_{timestamp}.csv'

        # Lưu file
        scraper.save_to_json(articles, json_filename)
        scraper.save_to_csv(articles, csv_filename)

        print(f"\n✓ Hoàn thành! Đã lưu {len(articles)} bài viết:")
        print(f"  - {json_filename}")
        print(f"  - {csv_filename}")

    except Exception as e:
        print(f"\n✗ Lỗi khi scrape: {e}")

    print(f"\nScrape tiếp theo vào: {datetime.now().strftime('%Y-%m-%d')} 09:00:00")


def main():
    """Hàm chính để chạy scheduler"""
    print("="*60)
    print("TrendForce Daily Scraper")
    print("="*60)
    print("\nLịch trình: Chạy mỗi ngày lúc 09:00")
    print("Nhấn Ctrl+C để dừng\n")

    # Đặt lịch chạy hàng ngày lúc 9:00 sáng
    schedule.every().day.at("09:00").do(run_daily_scrape)

    # Tùy chọn: Chạy ngay lần đầu tiên
    print("Chạy lần đầu tiên ngay bây giờ...")
    run_daily_scrape()

    # Vòng lặp chờ và chạy theo lịch
    while True:
        schedule.run_pending()
        time.sleep(60)  # Kiểm tra mỗi 60 giây


if __name__ == "__main__":
    main()
