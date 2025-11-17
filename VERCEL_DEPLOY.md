# Deploy lên Vercel - Hướng dẫn chi tiết

## Tổng quan

Project này bao gồm:
- ✅ Trang web tĩnh HTML/CSS/JS (Tailwind CSS)
- ✅ Hiển thị tin tức từ Supabase
- ✅ Serverless function để scrape (chạy theo lịch)
- ✅ Tự động deploy từ GitHub

---

## Bước 1: Chuẩn bị Supabase

### 1.1. Tạo table trong Supabase

1. Đăng nhập vào https://supabase.com
2. Chọn project: `aiorbvjphoslukcqvawx`
3. Click **SQL Editor** → **New query**
4. Copy & paste nội dung file [create_supabase_table.sql](create_supabase_table.sql)
5. Click **Run** (hoặc Ctrl+Enter)

**Kiểm tra:** Vào **Table Editor** → Xem table `trendforce_news` đã được tạo

### 1.2. Test insert data thử

Chạy local để test:

```bash
# Set environment variables
set SUPABASE_URL=https://aiorbvjphoslukcqvawx.supabase.co
set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Install dependencies
pip install -r requirements.txt

# Run scraper
python supabase_scraper.py
```

**Kiểm tra:** Vào Supabase Table Editor → Xem có data chưa

---

## Bước 2: Push code lên GitHub

### 2.1. Initialize Git (nếu chưa có)

```bash
cd "c:\Users\duong\Documents\trend forces rss"
git init
git add .
git commit -m "Initial commit - TrendForce scraper with Vercel"
```

### 2.2. Tạo repo trên GitHub

1. Vào https://github.com/new
2. Tạo repo mới tên `trendforce-news` (hoặc tên bạn muốn)
3. **Không** check "Initialize with README"
4. Click **Create repository**

### 2.3. Push code

```bash
git remote add origin https://github.com/YOUR_USERNAME/trendforce-news.git
git branch -M main
git push -u origin main
```

---

## Bước 3: Deploy lên Vercel

### 3.1. Import project

1. Truy cập https://vercel.com
2. Click **Add New** → **Project**
3. Import từ GitHub → Chọn repo `trendforce-news`

### 3.2. Configure Project

**Framework Preset:** Other (để trống)

**Build & Output Settings:**
- Build Command: (để trống)
- Output Directory: `public`
- Install Command: `pip install -r requirements.txt`

### 3.3. Environment Variables

Click **Environment Variables** và thêm:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://aiorbvjphoslukcqvawx.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |

**Lưu ý:** Paste FULL anon key vào

### 3.4. Deploy

Click **Deploy** và chờ ~1-2 phút

**Kết quả:** Bạn sẽ có URL dạng `https://trendforce-news-xxx.vercel.app`

---

## Bước 4: Kiểm tra deployment

### 4.1. Test trang web

Mở URL Vercel → Xem trang web có hiển thị không

**Nếu trống:** Có thể chưa có data trong Supabase

### 4.2. Test scraper API

Mở browser hoặc Postman:

```
GET https://trendforce-news-xxx.vercel.app/api/scrape
```

**Kết quả mong đợi:**
```json
{
  "success": true,
  "message": "Scraping completed successfully",
  "data": {
    "total": 27,
    "inserted": 27,
    "skipped": 0
  }
}
```

### 4.3. Refresh trang web

Sau khi scrape xong, refresh trang web → Xem tin tức đã hiển thị

---

## Bước 5: Setup Cron Job (Tự động scrape hàng ngày)

**Lưu ý:** Vercel Cron chỉ có trên **Pro plan** ($20/tháng)

### Nếu có Pro plan:

File `vercel.json` đã config sẵn:
```json
"crons": [
  {
    "path": "/api/scrape",
    "schedule": "0 9 * * *"
  }
]
```

→ Tự động chạy mỗi ngày lúc 9 AM UTC

### Nếu dùng Free plan - Alternative:

**Option A: GitHub Actions (Miễn phí)**

File `.github/workflows/scrape.yml` đã config sẵn, chỉ cần:

1. Vào GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
3. GitHub Actions sẽ tự động chạy mỗi ngày

**Option B: Cron-job.org (Miễn phí)**

1. Đăng ký tại https://cron-job.org
2. Tạo cron job mới:
   - URL: `https://trendforce-news-xxx.vercel.app/api/scrape`
   - Schedule: `0 9 * * *` (9 AM daily)

**Option C: UptimeRobot (Miễn phí)**

1. Đăng ký tại https://uptimerobot.com
2. Add monitor:
   - Type: HTTP(s)
   - URL: `https://trendforce-news-xxx.vercel.app/api/scrape`
   - Interval: Every 24 hours

---

## Bước 6: Custom Domain (Tùy chọn)

### 6.1. Thêm domain

1. Trong Vercel project → **Settings** → **Domains**
2. Add domain của bạn (vd: `trendforce.yourdomain.com`)
3. Thêm DNS records theo hướng dẫn

### 6.2. Update Supabase CORS

1. Vào Supabase → **Settings** → **API**
2. Scroll to **CORS**
3. Add domain Vercel của bạn

---

## Troubleshooting

### Trang web hiển thị trống

**Nguyên nhân:** Chưa có data trong Supabase

**Giải pháp:**
1. Gọi `/api/scrape` để scrape data
2. Hoặc chạy `python supabase_scraper.py` local

### Lỗi "Missing SUPABASE_URL or SUPABASE_KEY"

**Nguyên nhân:** Environment variables chưa set

**Giải pháp:**
1. Vào Vercel → Settings → Environment Variables
2. Add lại `SUPABASE_URL` và `SUPABASE_KEY`
3. Redeploy project

### Scraper timeout

**Nguyên nhân:** Vercel free tier timeout 10s, hobby 60s

**Giải pháp:**
- Giảm số trang scrape (trong `api/scrape.py` đổi `end_page=3` → `end_page=2`)
- Hoặc upgrade Vercel plan

### CORS error

**Nguyên nhân:** Supabase chặn request từ domain

**Giải pháp:**
1. Vào Supabase Settings → API → CORS
2. Add Vercel URL

---

## File Structure

```
trend forces rss/
├── public/
│   ├── index.html          # Trang chính
│   └── app.js              # JavaScript logic
├── api/
│   ├── scrape.py           # Serverless function
│   └── requirements.txt    # Python deps cho API
├── .github/
│   └── workflows/
│       └── scrape.yml      # GitHub Actions
├── vercel.json             # Vercel config
├── .vercelignore           # Files to ignore
├── supabase_scraper.py     # Scraper class
├── trendforce_scraper.py   # Core scraper
└── requirements.txt        # Python deps (local)
```

---

## Development Workflow

### Local development:

```bash
# Chạy scraper local
python supabase_scraper.py

# Test HTML (dùng Live Server hoặc)
python -m http.server 8000
# Mở http://localhost:8000/public/
```

### Deploy changes:

```bash
git add .
git commit -m "Update XYZ"
git push
```

→ Vercel tự động deploy!

---

## Monitoring

### Vercel Dashboard

- Vào project → **Deployments** → Xem logs
- Analytics → Xem traffic
- Functions → Xem scraper executions

### Supabase Dashboard

- Table Editor → Xem data
- Logs → Xem API calls
- Storage → Monitor usage

---

## Next Steps

Sau khi deploy xong, bạn có thể:

1. **Tùy chỉnh UI:**
   - Edit `public/index.html` và `public/app.js`
   - Thay đổi màu sắc, layout

2. **Thêm features:**
   - Filter theo category
   - Pagination
   - RSS feed
   - Newsletter signup

3. **SEO:**
   - Add meta tags
   - Sitemap
   - robots.txt

4. **Analytics:**
   - Add Google Analytics
   - Vercel Analytics (built-in)

---

## Support

- Vercel Docs: https://vercel.com/docs
- Supabase Docs: https://supabase.com/docs
- Tailwind CSS: https://tailwindcss.com/docs

🎉 Happy deploying!
