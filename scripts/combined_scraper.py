"""
Combined Scraper - Lấy tin từ cả News và Press Center
"""

import sys
import io

# Fix encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client
from trendforce_scraper import TrendForceScraper
from presscenter_scraper import PressCenterScraper

load_dotenv()


def main():
    """Scrape cả News và Press Center, lưu vào Supabase"""

    print("=" * 60)
    print("Combined Scraper: News + Press Center → Supabase")
    print("=" * 60)

    # Init Supabase
    supabase = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )

    all_articles = []

    # 1. Scrape News
    print("\n🗞️  Scraping TrendForce News...")
    news_scraper = TrendForceScraper()
    news_articles = news_scraper.scrape_multiple_pages(1, 3, delay=1.5)
    print(f"✅ Đã lấy {len(news_articles)} bài từ News")
    all_articles.extend(news_articles)

    # 2. Scrape Press Center
    print("\n📰 Scraping Press Center...")
    press_scraper = PressCenterScraper()
    press_articles = press_scraper.scrape_multiple_pages(1, 2, delay=1.5)
    print(f"✅ Đã lấy {len(press_articles)} bài từ Press Center")
    all_articles.extend(press_articles)

    # 3. Lưu vào Supabase
    print(f"\n💾 Đang lưu {len(all_articles)} bài viết vào Supabase...")

    inserted = 0
    skipped = 0
    errors = []

    for i, article in enumerate(all_articles, 1):
        try:
            # Check duplicate
            existing = supabase.table('trendforce_news')\
                .select('id')\
                .eq('url', article['url'])\
                .execute()

            if existing.data:
                skipped += 1
                print(f"⏭️  [{i}/{len(all_articles)}] Bỏ qua (trùng): {article['title'][:50]}...")
            else:
                # Insert
                supabase.table('trendforce_news').insert(article).execute()
                inserted += 1
                source = article.get('source', 'news')
                print(f"✅ [{i}/{len(all_articles)}] [{source}] Đã thêm: {article['title'][:50]}...")

        except Exception as e:
            errors.append({'title': article['title'], 'error': str(e)})
            print(f"❌ [{i}/{len(all_articles)}] Lỗi: {str(e)}")

    # Summary
    print(f"\n{'=' * 60}")
    print("📈 TỔNG KẾT")
    print(f"{'=' * 60}")
    print(f"📊 Tổng số bài: {len(all_articles)}")
    print(f"✅ Đã thêm mới: {inserted}")
    print(f"⏭️  Đã bỏ qua (trùng): {skipped}")
    if errors:
        print(f"❌ Lỗi: {len(errors)}")

    print(f"\n🎉 Hoàn thành!")


if __name__ == "__main__":
    main()
