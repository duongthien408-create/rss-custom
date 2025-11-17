# TrendForce News Scraper + Web Viewer

Full-stack solution để scrape, lưu trữ và hiển thị tin tức từ https://www.trendforce.com/news/

🌐 **Live Demo:** [Deploy lên Vercel](VERCEL_DEPLOY.md)
📊 **Database:** Supabase PostgreSQL

## Tính năng

- ✅ Scrape tin tức từ TrendForce bao gồm:
  - Tiêu đề bài viết
  - URL bài viết
  - Ngày đăng
  - Danh mục
  - Tóm tắt nội dung
  - Hình thumbnail
- ✅ Hỗ trợ scrape nhiều trang
- ✅ Xuất dữ liệu ra file JSON hoặc CSV
- ✅ **Lưu trực tiếp vào Supabase Database**
- ✅ **Web UI đẹp với Tailwind CSS** - Hiển thị tin tức real-time
- ✅ **Deploy lên Vercel** - Serverless, auto-scale
- ✅ Chạy tự động theo lịch (scheduled với cron)
- ✅ Search & filter tin tức
- ✅ Responsive design (mobile-friendly)
- ✅ Delay giữa các request để tránh quá tải server
- ✅ Tự động skip bài viết trùng lặp

## Cài đặt

1. Cài đặt Python (phiên bản 3.7 trở lên)

2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Cách sử dụng

### Cách 1: Chạy script mặc định

```bash
python trendforce_scraper.py
```

Script sẽ scrape trang đầu tiên và lưu vào file `trendforce_page1.json` và `trendforce_page1.csv`

### Cách 1.5: Chạy script ví dụ đầy đủ

```bash
python example_usage.py
```

Script này sẽ:
- Scrape trang 1 và lưu vào `output_page1.json`
- Scrape 5 trang đầu và lưu vào `output_5_pages.json` và `output_5_pages.csv`
- Hiển thị thống kê và 3 bài viết mới nhất

### Cách 2: Sử dụng trong code Python

```python
from trendforce_scraper import TrendForceScraper

# Khởi tạo scraper
scraper = TrendForceScraper()

# Scrape một trang
articles = scraper.scrape_page(1)

# Scrape nhiều trang (từ trang 1 đến trang 5)
all_articles = scraper.scrape_multiple_pages(start_page=1, end_page=5, delay=1.5)

# Lưu vào JSON
scraper.save_to_json(all_articles, 'output.json')

# Lưu vào CSV
scraper.save_to_csv(all_articles, 'output.csv')
```

### Ví dụ scrape nhiều trang

Mở file [trendforce_scraper.py](trendforce_scraper.py) và bỏ comment dòng 155-158:

```python
# Ví dụ 2: Scrape nhiều trang (uncommment để sử dụng)
print("\n=== Ví dụ 2: Scrape 3 trang đầu ===")
all_articles = scraper.scrape_multiple_pages(start_page=1, end_page=3, delay=1.5)
scraper.save_to_json(all_articles, 'trendforce_news_multiple.json')
scraper.save_to_csv(all_articles, 'trendforce_news_multiple.csv')
```

## Định dạng dữ liệu

Mỗi bài viết được lưu với các trường sau:

```json
{
  "title": "Tiêu đề bài viết",
  "url": "https://www.trendforce.com/news/...",
  "date": "2025-01-15",
  "category": "DRAM & Memory",
  "summary": "Tóm tắt nội dung bài viết...",
  "thumbnail": "https://img.trendforce.com/...",
  "scraped_at": "2025-01-17T10:30:00.123456"
}
```

## Lưu ý

- Script có delay mặc định 1 giây giữa các request để tôn trọng server
- Tổng số trang hiện tại là 787 (3,931 bài viết)
- Nên scrape từ từ và không quá nhiều trang cùng lúc
- Dữ liệu được lưu với encoding UTF-8 để hỗ trợ đầy đủ ký tự

## Tùy chỉnh

Bạn có thể thay đổi các tham số:

- `delay`: Thời gian chờ giữa các request (mặc định 1.0 giây)
- `start_page`, `end_page`: Phạm vi trang cần scrape
- Output filename: Tên file JSON/CSV đầu ra

## Chạy tự động theo lịch

### Cách nhanh nhất (Windows):

1. Double-click file `run_once.bat` để test
2. Thiết lập Windows Task Scheduler để chạy `run_once.bat` mỗi ngày

**Hoặc** sử dụng Python scheduler:

```bash
pip install schedule
python scheduled_scraper.py
```

Xem hướng dẫn chi tiết trong file [SCHEDULE_GUIDE.md](SCHEDULE_GUIDE.md)

### Test scheduler (chạy mỗi 30 giây):

```bash
python test_scheduler.py
```

## 🗄️ Lưu vào Supabase Database

### Setup nhanh:

1. **Tạo Supabase project** tại https://supabase.com
2. **Tạo table** bằng cách chạy SQL trong file [create_supabase_table.sql](create_supabase_table.sql)
3. **Lấy API keys** từ Settings → API
4. **Set environment variables:**
   ```bash
   set SUPABASE_URL=https://xxx.supabase.co
   set SUPABASE_KEY=your-anon-key
   ```
5. **Chạy scraper:**
   ```bash
   python supabase_scraper.py
   ```

**Xem hướng dẫn chi tiết:** [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

### Scheduled scraper với Supabase:

```bash
python supabase_scheduled.py
```

Tự động scrape mỗi ngày và lưu vào Supabase, tự động skip bài trùng!

## Yêu cầu hệ thống

- Python 3.7+
- Kết nối Internet
- Các thư viện: requests, beautifulsoup4, lxml, schedule
- Tùy chọn: supabase, python-dotenv (nếu dùng Supabase)
