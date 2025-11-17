# Hướng dẫn Setup Supabase

## Bước 1: Tạo Supabase Project

1. Truy cập https://supabase.com
2. Sign up hoặc Login
3. Click **"New Project"**
4. Điền thông tin:
   - **Name:** `trendforce-scraper` (hoặc tên bạn muốn)
   - **Database Password:** Tạo password mạnh
   - **Region:** Chọn gần bạn nhất
5. Click **"Create new project"** (chờ ~2 phút)

---

## Bước 2: Tạo Database Table

1. Trong project, click **"SQL Editor"** ở menu bên trái
2. Click **"New query"**
3. Copy toàn bộ nội dung file [create_supabase_table.sql](create_supabase_table.sql)
4. Paste vào SQL Editor
5. Click **"Run"** (hoặc Ctrl+Enter)

**Kết quả:** Table `trendforce_news` đã được tạo với các columns:
- `id` - Auto increment primary key
- `title` - Tiêu đề bài viết
- `url` - URL (unique, không trùng)
- `date` - Ngày đăng
- `category` - Danh mục
- `summary` - Tóm tắt
- `thumbnail` - Link hình
- `scraped_at` - Timestamp scrape
- `created_at` - Timestamp tạo record

---

## Bước 3: Lấy API Keys

1. Click **"Settings"** (icon bánh răng) ở menu trái
2. Click **"API"**
3. Scroll xuống phần **"Project API keys"**
4. Copy 2 giá trị:
   - **Project URL:** `https://xxx.supabase.co`
   - **anon public key:** `eyJhbG...` (một chuỗi rất dài)

---

## Bước 4: Cấu hình Local Environment

### Cách 1: Tạo file .env

1. Copy file `.env.example` thành `.env`:
   ```bash
   copy .env.example .env
   ```

2. Mở file `.env` và điền thông tin:
   ```
   SUPABASE_URL=https://xxx.supabase.co
   SUPABASE_KEY=eyJhbG...
   ```

3. Cài thêm python-dotenv:
   ```bash
   pip install python-dotenv
   ```

### Cách 2: Set Environment Variables (Windows)

```cmd
set SUPABASE_URL=https://xxx.supabase.co
set SUPABASE_KEY=eyJhbG...
```

**Lưu ý:** Cách này chỉ tồn tại trong session hiện tại.

Để set vĩnh viễn:
1. Nhấn `Win + R` → gõ `sysdm.cpl` → Enter
2. Tab **"Advanced"** → **"Environment Variables"**
3. Thêm 2 biến mới trong **"User variables"**

### Cách 3: Set Environment Variables (Linux/Mac)

```bash
export SUPABASE_URL=https://xxx.supabase.co
export SUPABASE_KEY=eyJhbG...
```

Thêm vào `~/.bashrc` hoặc `~/.zshrc` để lưu vĩnh viễn.

---

## Bước 5: Cài đặt Dependencies

```bash
pip install supabase python-dotenv
```

Hoặc:

```bash
pip install -r requirements.txt
```

---

## Bước 6: Test Kết Nối

Chạy script test:

```bash
python supabase_scraper.py
```

**Kết quả mong đợi:**
```
==================================================
TrendForce Scraper → Supabase
==================================================
🚀 Bắt đầu scrape từ trang 1 đến 3
...
✅ Đã thêm mới: 27
⏭️  Đã bỏ qua (trùng): 0
```

---

## Bước 7: Kiểm tra Data trong Supabase

1. Quay lại Supabase Dashboard
2. Click **"Table Editor"**
3. Chọn table **"trendforce_news"**
4. Xem các record đã được insert

---

## Chạy Scheduled Scraper với Supabase

### Chạy liên tục (Python Schedule):

```bash
python supabase_scheduled.py
```

Script sẽ:
- Chạy ngay lần đầu
- Tự động chạy lại mỗi ngày lúc 9:00 AM
- Lưu vào Supabase
- Tự động skip các bài đã tồn tại (dựa vào URL)

### Chạy với Task Scheduler (Windows):

Tạo file `.bat` mới:

```batch
@echo off
set SUPABASE_URL=https://xxx.supabase.co
set SUPABASE_KEY=eyJhbG...

cd /d "c:\Users\duong\Documents\trend forces rss"
python -c "from supabase_scraper import SupabaseScraper; s = SupabaseScraper(); s.scrape_and_save(1, 5)"
```

Sau đó thiết lập Task Scheduler chạy file `.bat` này mỗi ngày.

---

## Deploy lên Cloud (Tùy chọn)

### Deploy lên Vercel/Netlify với Cron

Tạo file `api/scrape.py` (serverless function):

```python
from supabase_scraper import SupabaseScraper

def handler(event, context):
    scraper = SupabaseScraper()
    result = scraper.scrape_and_save(1, 5)
    return {
        'statusCode': 200,
        'body': result
    }
```

Config cron trong `vercel.json`:

```json
{
  "crons": [{
    "path": "/api/scrape",
    "schedule": "0 9 * * *"
  }]
}
```

### Deploy lên Heroku

1. Tạo `Procfile`:
   ```
   worker: python supabase_scheduled.py
   ```

2. Deploy:
   ```bash
   heroku create
   heroku config:set SUPABASE_URL=xxx
   heroku config:set SUPABASE_KEY=xxx
   git push heroku main
   ```

### Deploy lên Railway/Render

Tương tự như Heroku, set environment variables và chạy `supabase_scheduled.py`

---

## Query Data từ Supabase

### Trong Python:

```python
from supabase_scraper import SupabaseScraper

scraper = SupabaseScraper()

# Lấy 10 bài mới nhất
latest = scraper.get_latest_articles(10)

# Tìm kiếm theo keyword
results = scraper.search_articles('NVIDIA')
```

### Từ Frontend (JavaScript):

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

// Lấy 10 bài mới nhất
const { data, error } = await supabase
  .from('trendforce_news')
  .select('*')
  .order('date', { ascending: false })
  .limit(10)
```

### Supabase REST API:

```bash
curl 'https://xxx.supabase.co/rest/v1/trendforce_news?select=*&order=date.desc&limit=10' \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

---

## Troubleshooting

### Lỗi "SUPABASE_URL và SUPABASE_KEY chưa set"

Kiểm tra lại environment variables:
```bash
echo %SUPABASE_URL%  # Windows
echo $SUPABASE_URL   # Linux/Mac
```

### Lỗi "relation trendforce_news does not exist"

Bạn chưa chạy SQL để tạo table. Quay lại Bước 2.

### Lỗi "duplicate key value violates unique constraint"

Bài viết đã tồn tại. Script sẽ tự động skip.

### Lỗi "Invalid API key"

Kiểm tra lại SUPABASE_KEY, phải copy đúng từ Settings → API

---

## Tính năng nâng cao

### 1. Auto-delete old records (giữ 1000 bài mới nhất)

Thêm vào scheduled function:

```python
# Delete old records, keep only 1000 newest
scraper.supabase.rpc('delete_old_news', {'keep_count': 1000}).execute()
```

SQL function:
```sql
CREATE OR REPLACE FUNCTION delete_old_news(keep_count INT)
RETURNS void AS $$
BEGIN
  DELETE FROM trendforce_news
  WHERE id NOT IN (
    SELECT id FROM trendforce_news
    ORDER BY date DESC, id DESC
    LIMIT keep_count
  );
END;
$$ LANGUAGE plpgsql;
```

### 2. RSS Feed từ Supabase

Tạo Edge Function để export RSS:

```typescript
// supabase/functions/rss/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from '@supabase/supabase-js'

serve(async (req) => {
  const supabase = createClient(...)
  const { data } = await supabase
    .from('trendforce_news')
    .select('*')
    .order('date', { ascending: false })
    .limit(50)

  const rss = generateRSS(data)
  return new Response(rss, {
    headers: { 'Content-Type': 'application/xml' }
  })
})
```

### 3. Real-time Notifications

Subscribe to new inserts:

```javascript
supabase
  .channel('news-changes')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'trendforce_news' },
    (payload) => console.log('New article!', payload)
  )
  .subscribe()
```

---

## Best Practices

1. **Sử dụng Service Role Key** cho scheduled jobs (không public)
2. **Enable RLS** để bảo vệ data
3. **Tạo indexes** cho các columns hay query
4. **Backup định kỳ** (Supabase tự động backup, nhưng nên export thêm)
5. **Monitor usage** trong Supabase Dashboard → Settings → Usage
