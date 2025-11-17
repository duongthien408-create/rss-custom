"""
TrendForce News Scraper
Script để lấy nội dung tin tức từ https://www.trendforce.com/news/
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


class TrendForceScraper:
    """Class để scrape tin tức từ TrendForce"""

    def __init__(self):
        self.base_url = "https://www.trendforce.com/news"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def scrape_page(self, page_number: int = 1) -> List[Dict]:
        """
        Scrape một trang tin tức

        Args:
            page_number: Số trang cần scrape (mặc định là 1)

        Returns:
            List các dict chứa thông tin bài viết
        """
        if page_number == 1:
            url = self.base_url
        else:
            url = f"{self.base_url}/page/{page_number}/"

        print(f"Đang scrape trang {page_number}: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Lỗi khi tải trang: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        seen_urls = set()  # Để tránh trùng lặp

        # Tìm tất cả các links có text và chứa /news/ trong href
        all_links = soup.find_all('a', href=True)

        for link in all_links:
            href = link.get('href', '')

            # Chỉ lấy link bài viết news (có pattern /news/YYYY/MM/DD/)
            # Bỏ qua link category và link /news/ chính
            if '/news/' not in href or href == '/news/':
                continue

            # Bỏ qua link category
            if '/news/category/' in href:
                continue

            # Bỏ qua link pagination
            if '/news/page/' in href:
                continue

            # Chỉ lấy link có text (title), bỏ qua link hình ảnh
            link_text = link.get_text(strip=True)
            if not link_text:
                continue

            # Bỏ qua link có text là số hoặc "First Page", "Last Page", etc
            if link_text.isdigit() or 'page' in link_text.lower():
                continue

            # Đảm bảo URL đầy đủ
            if not href.startswith('http'):
                article_url = 'https://www.trendforce.com' + href
            else:
                article_url = href

            # Tránh trùng lặp
            if article_url in seen_urls:
                continue
            seen_urls.add(article_url)

            title = link_text

            # Tìm parent container của link để lấy thêm thông tin
            container = link.find_parent(['div', 'article', 'li'])

            date = ''
            category = ''
            summary = ''
            thumbnail = ''

            # Tìm thumbnail - có thể trong sibling link hoặc parent
            # Thử tìm img trong tất cả các <a> tag có cùng URL
            for a_tag in soup.find_all('a', href=href):
                img = a_tag.find('img')
                if img:
                    thumbnail = img.get('src', '') or img.get('data-src', '')
                    if thumbnail:
                        break

            if container:
                # Tìm date
                import re
                date_elem = container.find('span', class_=lambda x: x and 'date' in str(x).lower())
                if not date_elem:
                    date_elem = container.find('time')
                if not date_elem:
                    # Tìm từ URL nếu có pattern /YYYY/MM/DD/
                    url_date_match = re.search(r'/(\d{4}/\d{2}/\d{2})/', article_url)
                    if url_date_match:
                        date = url_date_match.group(1).replace('/', '-')
                    else:
                        # Tìm text có pattern YYYY-MM-DD
                        text = container.get_text()
                        date_match = re.search(r'\d{4}-\d{2}-\d{2}', text)
                        if date_match:
                            date = date_match.group()
                if date_elem and not date:
                    date = date_elem.get_text(strip=True)

                # Tìm category từ URL
                category_match = re.search(r'/news/category/([^/]+)/', article_url)
                if category_match:
                    category = category_match.group(1).replace('-', ' ').title()

                # Tìm summary
                summary_elem = container.find(['p', 'div'], class_=lambda x: x and ('excerpt' in str(x).lower() or 'summary' in str(x).lower()))
                if not summary_elem:
                    # Tìm thẻ p nào không phải là link
                    for p in container.find_all('p'):
                        p_text = p.get_text(strip=True)
                        if p_text and len(p_text) > 20:  # Chỉ lấy summary có độ dài hợp lý
                            summary = p_text
                            break
                else:
                    summary = summary_elem.get_text(strip=True)

            article = {
                'title': title,
                'url': article_url,
                'date': date,
                'category': category,
                'summary': summary,
                'thumbnail': thumbnail,
                'scraped_at': datetime.now().isoformat()
            }

            articles.append(article)

        print(f"Đã tìm thấy {len(articles)} bài viết trên trang {page_number}")
        return articles

    def scrape_multiple_pages(self, start_page: int = 1, end_page: int = 1, delay: float = 1.0) -> List[Dict]:
        """
        Scrape nhiều trang tin tức

        Args:
            start_page: Trang bắt đầu
            end_page: Trang kết thúc
            delay: Thời gian chờ giữa các request (giây)

        Returns:
            List tất cả các bài viết
        """
        all_articles = []

        for page in range(start_page, end_page + 1):
            articles = self.scrape_page(page)
            all_articles.extend(articles)

            # Chờ một chút để tránh quá tải server
            if page < end_page:
                time.sleep(delay)

        print(f"\nTổng cộng đã scrape {len(all_articles)} bài viết từ {end_page - start_page + 1} trang")
        return all_articles

    def save_to_json(self, articles: List[Dict], filename: str = 'trendforce_news.json'):
        """Lưu dữ liệu vào file JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu {len(articles)} bài viết vào {filename}")

    def save_to_csv(self, articles: List[Dict], filename: str = 'trendforce_news.csv'):
        """Lưu dữ liệu vào file CSV"""
        if not articles:
            print("Không có dữ liệu để lưu")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'url', 'date', 'category', 'summary', 'thumbnail', 'scraped_at']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(articles)

        print(f"Đã lưu {len(articles)} bài viết vào {filename}")


def main():
    """Hàm chính để chạy script"""
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    scraper = TrendForceScraper()

    # Ví dụ 1: Scrape trang đầu tiên
    print("=== Ví dụ 1: Scrape trang 1 ===")
    articles = scraper.scrape_page(1)

    if articles:
        print(f"\nBài viết đầu tiên:")
        print(f"Tiêu đề: {articles[0]['title']}")
        print(f"URL: {articles[0]['url']}")
        print(f"Ngày: {articles[0]['date']}")
        print(f"Danh mục: {articles[0]['category']}")
        print(f"Tóm tắt: {articles[0]['summary'][:100]}...")

        # Lưu vào file
        scraper.save_to_json(articles, 'trendforce_page1.json')
        scraper.save_to_csv(articles, 'trendforce_page1.csv')

    # Ví dụ 2: Scrape nhiều trang (uncommment để sử dụng)
    # print("\n=== Ví dụ 2: Scrape 3 trang đầu ===")
    # all_articles = scraper.scrape_multiple_pages(start_page=1, end_page=3, delay=1.5)
    # scraper.save_to_json(all_articles, 'trendforce_news_multiple.json')
    # scraper.save_to_csv(all_articles, 'trendforce_news_multiple.csv')


if __name__ == "__main__":
    main()
