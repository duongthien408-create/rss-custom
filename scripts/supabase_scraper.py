"""
TrendForce Scraper với Supabase integration
Scrape tin tức và lưu vào Supabase database
"""

import os
from datetime import datetime
from typing import List, Dict
from trendforce_scraper import TrendForceScraper

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Không cần thiết nếu không có .env

try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Chưa cài đặt supabase library!")
    print("Chạy: pip install supabase")
    exit(1)


class SupabaseScraper:
    """Class để scrape và lưu vào Supabase"""

    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        """
        Khởi tạo Supabase client

        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anon/service key
        """
        # Lấy từ environment variables hoặc params
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_KEY')

        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Cần có SUPABASE_URL và SUPABASE_KEY!\n"
                "Có thể set qua environment variables hoặc truyền vào constructor.\n"
                "Ví dụ:\n"
                "  export SUPABASE_URL='https://xxx.supabase.co'\n"
                "  export SUPABASE_KEY='your-anon-key'"
            )

        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.scraper = TrendForceScraper()

    def scrape_and_save(self, start_page: int = 1, end_page: int = 3,
                       table_name: str = 'trendforce_news') -> Dict:
        """
        Scrape tin tức và lưu vào Supabase

        Args:
            start_page: Trang bắt đầu
            end_page: Trang kết thúc
            table_name: Tên bảng trong Supabase

        Returns:
            Dict với thống kê kết quả
        """
        print(f"🚀 Bắt đầu scrape từ trang {start_page} đến {end_page}")

        # Scrape articles
        articles = self.scraper.scrape_multiple_pages(
            start_page=start_page,
            end_page=end_page,
            delay=1.5
        )

        if not articles:
            print("❌ Không có bài viết nào được scrape!")
            return {'success': False, 'total': 0, 'inserted': 0, 'skipped': 0}

        print(f"\n📊 Đã scrape {len(articles)} bài viết")
        print(f"💾 Đang lưu vào Supabase table: {table_name}")

        # Lưu từng article vào Supabase
        inserted = 0
        skipped = 0
        errors = []

        for i, article in enumerate(articles, 1):
            try:
                # Kiểm tra xem bài viết đã tồn tại chưa (dựa vào URL)
                existing = self.supabase.table(table_name)\
                    .select('id')\
                    .eq('url', article['url'])\
                    .execute()

                if existing.data:
                    skipped += 1
                    print(f"⏭️  [{i}/{len(articles)}] Bỏ qua (đã tồn tại): {article['title'][:50]}...")
                else:
                    # Insert article mới
                    self.supabase.table(table_name).insert(article).execute()
                    inserted += 1
                    print(f"✅ [{i}/{len(articles)}] Đã thêm: {article['title'][:50]}...")

            except Exception as e:
                errors.append({'article': article['title'], 'error': str(e)})
                print(f"❌ [{i}/{len(articles)}] Lỗi: {str(e)}")

        # Tổng kết
        print(f"\n{'='*60}")
        print(f"📈 TỔNG KẾT")
        print(f"{'='*60}")
        print(f"✅ Đã thêm mới: {inserted}")
        print(f"⏭️  Đã bỏ qua (trùng): {skipped}")
        if errors:
            print(f"❌ Lỗi: {len(errors)}")

        return {
            'success': True,
            'total': len(articles),
            'inserted': inserted,
            'skipped': skipped,
            'errors': errors
        }

    def get_latest_articles(self, limit: int = 10, table_name: str = 'trendforce_news') -> List[Dict]:
        """
        Lấy các bài viết mới nhất từ Supabase

        Args:
            limit: Số lượng bài viết
            table_name: Tên bảng

        Returns:
            List các bài viết
        """
        result = self.supabase.table(table_name)\
            .select('*')\
            .order('date', desc=True)\
            .limit(limit)\
            .execute()

        return result.data

    def search_articles(self, keyword: str, table_name: str = 'trendforce_news') -> List[Dict]:
        """
        Tìm kiếm bài viết theo từ khóa

        Args:
            keyword: Từ khóa tìm kiếm
            table_name: Tên bảng

        Returns:
            List các bài viết tìm thấy
        """
        result = self.supabase.table(table_name)\
            .select('*')\
            .ilike('title', f'%{keyword}%')\
            .execute()

        return result.data


def main():
    """Hàm chính"""
    print("="*60)
    print("TrendForce Scraper → Supabase")
    print("="*60)

    # Kiểm tra environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        print("\n⚠️  Chưa set SUPABASE_URL và SUPABASE_KEY!")
        print("\nCách set (Windows):")
        print('  set SUPABASE_URL=https://xxx.supabase.co')
        print('  set SUPABASE_KEY=your-anon-key')
        print("\nCách set (Linux/Mac):")
        print('  export SUPABASE_URL=https://xxx.supabase.co')
        print('  export SUPABASE_KEY=your-anon-key')
        print("\nHoặc tạo file .env (xem .env.example)")
        return

    try:
        # Khởi tạo scraper
        scraper = SupabaseScraper(supabase_url, supabase_key)

        # Scrape và lưu vào Supabase
        result = scraper.scrape_and_save(
            start_page=1,
            end_page=3,  # Scrape 3 trang đầu
            table_name='trendforce_news'
        )

        if result['success']:
            print("\n🎉 Hoàn thành!")

            # Hiển thị 3 bài mới nhất từ database
            print(f"\n{'='*60}")
            print("📰 3 BÀI MỚI NHẤT TRONG DATABASE")
            print(f"{'='*60}")

            latest = scraper.get_latest_articles(limit=3)
            for i, article in enumerate(latest, 1):
                print(f"\n{i}. {article['title']}")
                print(f"   📅 {article['date']}")
                print(f"   🔗 {article['url']}")

    except ValueError as e:
        print(f"\n❌ Lỗi: {e}")
    except Exception as e:
        print(f"\n❌ Lỗi không xác định: {e}")


if __name__ == "__main__":
    main()
