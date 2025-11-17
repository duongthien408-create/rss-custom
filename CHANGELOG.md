# Changelog - TrendForce News RSS

## 2025-11-18 - Major Update 🎉

### Tóm tắt
Hoàn thành hệ thống scraping tự động, lưu trữ, và hiển thị tin tức từ TrendForce với giao diện web đẹp mắt và hỗ trợ đa nguồn (News + Press Release).

---

### 1. Web Scraping System

#### ✅ TrendForce News Scraper
- **File**: `scripts/trendforce_scraper.py`
- **Nguồn**: https://www.trendforce.com/news/
- **Tính năng**:
  - Scrape title, URL, date, category, summary, thumbnail
  - Hỗ trợ scrape nhiều trang với delay
  - Extract article_id từ URL pattern
  - Export JSON/CSV
  - Windows encoding support (UTF-8)

#### ✅ Press Center Scraper
- **File**: `scripts/presscenter_scraper.py`
- **Nguồn**: https://www.trendforce.com/presscenter/news
- **Tính năng**:
  - Scrape Press Release articles
  - Parse date format: "17 November 2025" → "2025-11-17"
  - HTML structure khác với News (h3 → h4 → p)
  - Source tag: 'presscenter'

#### ✅ Combined Scraper
- **File**: `scripts/combined_scraper.py`
- **Tính năng**:
  - Gộp cả News (3 pages) + Press Center (2 pages)
  - Tự động check duplicate trước khi insert
  - Upload trực tiếp vào Supabase
  - Kết quả test: 27 News + 10 Press Release = **37 articles**

---

### 2. Database - Supabase PostgreSQL

#### ✅ Schema Design
**Table**: `trendforce_news`

Columns chính:
- `id` - Primary key (auto-increment)
- `title` - Tiêu đề bài viết (EN)
- `url` - Link bài viết (unique)
- `date` - Ngày đăng
- `category` - Danh mục
- `summary` - Tóm tắt (EN)
- `thumbnail` - Link ảnh thumbnail
- `scraped_at` - Timestamp khi scrape

Columns mở rộng (Phase 2):
- `title_vi` - Tiêu đề tiếng Việt
- `summary_vi` - Tóm tắt tiếng Việt
- `translated_at` - Timestamp dịch
- `article_id` - ID extract từ URL
- `source` - Nguồn: 'news' hoặc 'presscenter'

#### ✅ Indexes
- `idx_trendforce_news_url` - Unique URL
- `idx_trendforce_news_date` - Sort by date
- `idx_trendforce_news_title_vi` - Full-text search tiếng Việt
- `idx_trendforce_news_article_id` - Fast lookup
- `idx_trendforce_news_source` - Filter by source

#### ✅ Configuration
- **RLS (Row Level Security)**: Disabled for easier access
- **Supabase URL**: https://aiorbvjphoslukcqvawx.supabase.co
- Migration files: `sql/`

---

### 3. Frontend - Tailwind CSS + Vanilla JS

#### ✅ Features
**File**: `public/index.html`, `public/app.js`

- **Stats Dashboard**:
  - Total articles
  - Today's articles
  - This week's articles
  - Source count

- **Filter System**:
  - 📊 **All** - Tất cả bài viết
  - 🗞️ **News** - Chỉ bài từ /news/
  - 📰 **Press Release** - Chỉ bài từ /presscenter/
  - Hiển thị số lượng real-time

- **Source Badges**:
  - 🗞️ Blue badge cho News
  - 📰 Purple badge cho Press Release
  - 🇻🇳 Green badge cho bài đã dịch tiếng Việt

- **Search & Sort**:
  - Real-time search (title + summary, cả EN và VI)
  - Sort: Newest First / Oldest First / Title A-Z
  - Debounced input (300ms)

- **UI/UX**:
  - Responsive grid (1/2/3 columns)
  - Card hover effects
  - Skeleton loading states
  - Empty/Error states
  - Gradient header
  - Thumbnail support with fallback

#### ✅ Vietnamese Translation Support
- Ưu tiên hiển thị `title_vi` nếu có, fallback sang `title`
- Ưu tiên hiển thị `summary_vi` nếu có, fallback sang `summary`
- Badge 🇻🇳 hiển thị khi có bản dịch
- Tích hợp sẵn cho n8n workflow (update từ bên ngoài)

---

### 4. Deployment & Automation

#### ✅ Vercel Deployment
- **File**: `vercel.json`
- **Static hosting**: `public/` folder
- **Serverless API**: `api/scrape.py`
- **Cron Job**: Chạy lúc 15:00 UTC = **22:00 giờ Việt Nam** mỗi ngày
- **Auto-deploy**: Push to GitHub → Auto deploy
- **URL**: [sẽ có sau khi deploy]

#### ✅ GitHub Actions
- **File**: `.github/workflows/scrape.yml`
- **Schedule**: `0 15 * * *` (10 PM Vietnam time)
- **Manual trigger**: workflow_dispatch
- **Secrets cần thiết**:
  - `SUPABASE_URL`
  - `SUPABASE_KEY`

#### ✅ API Endpoint
- **Path**: `/api/scrape`
- **Method**: GET
- **Function**: Chạy `combined_scraper.py` serverless
- **Response**: JSON status

---

### 5. Code Organization

#### ✅ Folder Structure
```
trend-forces-rss/
├── .github/workflows/     # GitHub Actions
├── api/                   # Vercel serverless functions
├── archive/              # Old test files & outputs
├── docs/                 # Documentation (guides, setup)
├── public/               # Frontend (HTML, CSS, JS)
├── scripts/              # Python scrapers
├── sql/                  # Database migrations
├── .env                  # Environment variables (gitignored)
├── .gitignore
├── README.md
├── CHANGELOG.md          # This file
├── ROADMAP.md            # Future plans
├── requirements.txt      # Python dependencies
└── vercel.json           # Vercel config
```

#### ✅ Key Scripts
- `scripts/trendforce_scraper.py` - News scraper
- `scripts/presscenter_scraper.py` - Press Release scraper
- `scripts/combined_scraper.py` - **Main scraper** (gộp cả 2)
- `scripts/supabase_scraper.py` - Legacy standalone version
- `archive/test_vietnamese_update.py` - Test Vietnamese updates

---

### 6. Bug Fixes & Improvements

#### ✅ Encoding Issues (Windows)
- **Problem**: `UnicodeEncodeError` khi print Vietnamese text trên Windows
- **Solution**: Wrap stdout/stderr với UTF-8 TextIOWrapper
- **Location**: Di chuyển vào `main()` function để tránh conflict khi import

#### ✅ Supabase RLS
- **Problem**: Row-level security block inserts
- **Solution**: Disabled RLS (hoặc tạo policy allow all)

#### ✅ Missing Columns
- **Problem**: `article_id` và `source` chưa có trong DB
- **Solution**: Chạy migration `sql/add_article_id_column.sql`

#### ✅ Thumbnail Extraction
- **Problem**: Ban đầu không tìm được thumbnail
- **Solution**: Scan tất cả `<a>` tags có cùng href, tìm `<img>` bên trong

---

### 7. Testing & Validation

#### ✅ Test Results
- ✅ Scraped 27 News articles successfully
- ✅ Scraped 10 Press Release articles successfully
- ✅ Combined scraper: 37/37 articles processed
- ✅ Duplicate detection working (0 duplicates on re-run)
- ✅ Vietnamese update test passed
- ✅ Frontend filter tabs working
- ✅ Source badges displaying correctly
- ✅ Search across both EN and VI fields working

---

### 8. Documentation

#### ✅ Guides Created
- `docs/DEPLOYMENT.md` - Deployment guide
- `docs/QUICK_START_SCHEDULER.md` - Scheduler quick start
- `docs/SCHEDULE_GUIDE.md` - Detailed scheduling guide
- `docs/SUPABASE_SETUP.md` - Database setup
- `docs/VERCEL_DEPLOY.md` - Vercel deployment
- `README.md` - Project overview
- `CHANGELOG.md` - This file
- `ROADMAP.md` - Future plans

---

## Statistics

- **Total commits**: ~15+
- **Total files**: 50+ (before cleanup)
- **Total files after cleanup**: ~25
- **Lines of Python**: ~500+
- **Lines of JavaScript**: ~330
- **Database records**: 37 articles
- **Sources integrated**: 2 (News + Press Center)
- **Languages supported**: 2 (English + Vietnamese)

---

## Contributors

- **Developer**: Claude (AI Assistant)
- **Project Owner**: @duongthien408-create
- **Repo**: https://github.com/duongthien408-create/rss-custom

---

## Tech Stack

- **Backend**: Python 3.x (BeautifulSoup4, Requests, Supabase client)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: Vanilla JavaScript, Tailwind CSS
- **Deployment**: Vercel (Static + Serverless)
- **CI/CD**: GitHub Actions
- **Translation** (planned): n8n + AI (GPT/Claude)

---

Generated on: 2025-11-18
