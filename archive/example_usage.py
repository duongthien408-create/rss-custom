"""
Script ví dụ sử dụng TrendForce Scraper
Chạy: python example_usage.py
"""

from trendforce_scraper import TrendForceScraper

def main():
    scraper = TrendForceScraper()

    # ===== VÍ DỤ 1: Scrape 1 trang =====
    print("=" * 60)
    print("VÍ DỤ 1: Scrape trang đầu tiên")
    print("=" * 60)

    articles = scraper.scrape_page(1)
    scraper.save_to_json(articles, 'output_page1.json')
    print(f"✓ Đã lưu {len(articles)} bài viết vào output_page1.json\n")

    # ===== VÍ DỤ 2: Scrape nhiều trang =====
    print("=" * 60)
    print("VÍ DỤ 2: Scrape 5 trang đầu tiên")
    print("=" * 60)

    articles = scraper.scrape_multiple_pages(
        start_page=1,
        end_page=5,
        delay=1.5  # Chờ 1.5 giây giữa các request
    )

    scraper.save_to_json(articles, 'output_5_pages.json')
    scraper.save_to_csv(articles, 'output_5_pages.csv')

    print(f"\n✓ Đã lưu {len(articles)} bài viết vào:")
    print(f"  - output_5_pages.json")
    print(f"  - output_5_pages.csv")

    # Hiển thị một số thống kê
    print(f"\n{'=' * 60}")
    print("THỐNG KÊ")
    print("=" * 60)

    articles_with_summary = [a for a in articles if a['summary']]
    print(f"Tổng số bài viết: {len(articles)}")
    print(f"Bài viết có summary: {len(articles_with_summary)}")

    # Hiển thị 3 bài mới nhất
    print(f"\n3 BÀI VIẾT MỚI NHẤT:")
    print("-" * 60)
    for i, article in enumerate(articles[:3], 1):
        print(f"\n{i}. {article['title'][:70]}...")
        print(f"   URL: {article['url']}")
        print(f"   Ngày: {article['date']}")
        if article['summary']:
            print(f"   Tóm tắt: {article['summary'][:100]}...")


if __name__ == "__main__":
    main()
