"""
Script chạy scheduled scraper và lưu vào Supabase
Chạy tự động hàng ngày
"""

import schedule
import time
from datetime import datetime
from supabase_scraper import SupabaseScraper


def run_daily_supabase_scrape():
    """Hàm chạy scrape hàng ngày và lưu vào Supabase"""
    print(f"\n{'='*60}")
    print(f"🚀 Bắt đầu scrape lúc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        scraper = SupabaseScraper()

        # Scrape và lưu vào Supabase
        result = scraper.scrape_and_save(
            start_page=1,
            end_page=5,  # Scrape 5 trang mỗi ngày
            table_name='trendforce_news'
        )

        if result['success']:
            print(f"\n✅ Hoàn thành!")
            print(f"   - Thêm mới: {result['inserted']} bài")
            print(f"   - Bỏ qua: {result['skipped']} bài")
        else:
            print(f"\n❌ Scrape thất bại!")

    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

    print(f"\n⏰ Scrape tiếp theo vào: ngày mai lúc 09:00")


def main():
    """Hàm chính để chạy scheduler"""
    print("="*60)
    print("TrendForce → Supabase Daily Scraper")
    print("="*60)
    print("\n⏰ Lịch trình: Chạy mỗi ngày lúc 09:00")
    print("⌨️  Nhấn Ctrl+C để dừng\n")

    # Đặt lịch chạy hàng ngày lúc 9:00
    schedule.every().day.at("09:00").do(run_daily_supabase_scrape)

    # Tùy chọn: Chạy ngay lần đầu tiên
    print("🎯 Chạy lần đầu tiên ngay bây giờ...")
    run_daily_supabase_scrape()

    # Vòng lặp
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
