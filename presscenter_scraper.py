"""
TrendForce Press Center Scraper
Scrape tin tức từ https://www.trendforce.com/presscenter/news
"""

import sys
import io
import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from typing import List, Dict
import time
import re


class PressCenterScraper:
    """Class để scrape Press Center"""

    def __init__(self):
        self.base_url = "https://www.trendforce.com/presscenter/news"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_page(self, page_number: int = 1) -> List[Dict]:
        """
        Scrape một trang press center

        Args:
            page_number: Số trang

        Returns:
            List các dict chứa thông tin bài viết
        """
        if page_number == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}?page={page_number}"

        print(f"Đang scrape trang {page_number}: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Lỗi khi tải trang: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        # Tìm tất cả thẻ h3 chứa title
        h3_tags = soup.find_all('h3')

        for h3 in h3_tags:
            try:
                # Tìm link bài viết trong h3
                link = h3.find('a', href=True)
                if not link:
                    continue

                href = link.get('href', '')

                # Chỉ lấy link press center
                if '/presscenter/news/' not in href:
                    continue

                # Đảm bảo URL đầy đủ
                if not href.startswith('http'):
                    article_url = 'https://www.trendforce.com' + href
                else:
                    article_url = href

                title = link.get_text(strip=True)

                # Tìm date (h4 tiếp theo sau h3)
                date = ''
                h4 = h3.find_next_sibling('h4')
                if h4:
                    date_text = h4.get_text(strip=True)
                    # Parse date: "17 November 2025" -> "2025-11-17"
                    try:
                        date_obj = datetime.strptime(date_text, '%d %B %Y')
                        date = date_obj.strftime('%Y-%m-%d')
                    except:
                        date = date_text

                # Tìm summary (p tiếp theo sau h4)
                summary = ''
                if h4:
                    p = h4.find_next_sibling('p')
                    if p:
                        summary = p.get_text(strip=True)

                # Extract ID từ URL
                url_match = re.search(r'/(\d{8})-(\d+)\.html', article_url)
                article_id = url_match.group(2) if url_match else ''

                article = {
                    'title': title,
                    'url': article_url,
                    'date': date,
                    'category': 'Press Release',
                    'summary': summary,
                    'thumbnail': '',  # Press center không có thumbnail
                    'article_id': article_id,
                    'scraped_at': datetime.now().isoformat(),
                    'source': 'presscenter'
                }

                articles.append(article)

            except Exception as e:
                print(f"Lỗi khi parse bài viết: {e}")
                continue

        print(f"Đã tìm thấy {len(articles)} bài viết trên trang {page_number}")
        return articles

    def scrape_multiple_pages(self, start_page: int = 1, end_page: int = 1, delay: float = 1.0) -> List[Dict]:
        """Scrape nhiều trang"""
        all_articles = []

        for page in range(start_page, end_page + 1):
            articles = self.scrape_page(page)
            all_articles.extend(articles)

            if page < end_page:
                time.sleep(delay)

        print(f"\nTổng cộng đã scrape {len(all_articles)} bài viết từ {end_page - start_page + 1} trang")
        return all_articles

    def save_to_json(self, articles: List[Dict], filename: str = 'presscenter_news.json'):
        """Lưu dữ liệu vào file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu {len(articles)} bài viết vào {filename}")

    def save_to_csv(self, articles: List[Dict], filename: str = 'presscenter_news.csv'):
        """Lưu dữ liệu vào file CSV"""
        if not articles:
            print("Không có dữ liệu để lưu")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'url', 'date', 'category', 'summary', 'thumbnail', 'article_id', 'source', 'scraped_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(articles)

        print(f"Đã lưu {len(articles)} bài viết vào {filename}")


def main():
    """Hàm chính"""
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    scraper = PressCenterScraper()

    print("=" * 60)
    print("TrendForce Press Center Scraper")
    print("=" * 60)

    # Scrape trang đầu tiên
    articles = scraper.scrape_page(1)

    if articles:
        print(f"\nBài viết đầu tiên:")
        print(f"Tiêu đề: {articles[0]['title']}")
        print(f"URL: {articles[0]['url']}")
        print(f"Ngày: {articles[0]['date']}")
        print(f"Tóm tắt: {articles[0]['summary'][:100]}...")

        # Lưu vào file
        scraper.save_to_json(articles, 'presscenter_page1.json')
        scraper.save_to_csv(articles, 'presscenter_page1.csv')


if __name__ == "__main__":
    main()
