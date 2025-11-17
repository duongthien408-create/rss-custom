# Deployment Options - Deploy scraper lên cloud

Có nhiều cách để deploy scraper này lên cloud để chạy tự động 24/7.

---

## Option 1: Railway (Khuyến nghị - Miễn phí $5/tháng)

### Ưu điểm:
- ✅ Free tier $5/tháng (đủ cho project này)
- ✅ Rất dễ setup
- ✅ Tự động deploy từ GitHub
- ✅ Support cron jobs

### Setup:

1. **Push code lên GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/trendforce-scraper.git
   git push -u origin main
   ```

2. **Deploy lên Railway:**
   - Truy cập https://railway.app
   - Login với GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Chọn repo vừa tạo
   - Add environment variables:
     ```
     SUPABASE_URL=https://xxx.supabase.co
     SUPABASE_KEY=your-key
     ```

3. **Tạo file `railway.json`:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python supabase_scheduled.py",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

4. **Deploy:** Railway sẽ tự động build và chạy!

---

## Option 2: Render (Miễn phí với hạn chế)

### Ưu điểm:
- ✅ Free tier
- ✅ Dễ setup
- ✅ Support cron jobs

### Nhược điểm:
- ❌ Free tier spin down sau 15 phút không dùng
- ❌ 750 giờ/tháng (đủ chạy cron daily)

### Setup:

1. **Tạo file `render.yaml`:**
   ```yaml
   services:
     - type: cron
       name: trendforce-scraper
       env: python
       schedule: "0 9 * * *"  # 9 AM daily
       buildCommand: "pip install -r requirements.txt"
       startCommand: "python -c 'from supabase_scraper import SupabaseScraper; s = SupabaseScraper(); s.scrape_and_save(1, 5)'"
       envVars:
         - key: SUPABASE_URL
           sync: false
         - key: SUPABASE_KEY
           sync: false
   ```

2. **Deploy:**
   - Truy cập https://render.com
   - New → Blueprint
   - Connect GitHub repo
   - Set environment variables

---

## Option 3: Vercel Cron (Serverless)

### Ưu điểm:
- ✅ Free tier generous
- ✅ Serverless (chỉ chạy khi cần)
- ✅ Rất nhanh

### Nhược điểm:
- ❌ Timeout 10s (hobby), 60s (pro)
- ❌ Cần viết lại thành serverless function

### Setup:

1. **Tạo `api/scrape.py`:**
   ```python
   from http.server import BaseHTTPRequestHandler
   from supabase_scraper import SupabaseScraper

   class handler(BaseHTTPRequestHandler):
       def do_GET(self):
           scraper = SupabaseScraper()
           result = scraper.scrape_and_save(1, 2)  # Chỉ 2 trang để tránh timeout

           self.send_response(200)
           self.send_header('Content-type', 'application/json')
           self.end_headers()
           self.wfile.write(str(result).encode())
           return
   ```

2. **Tạo `vercel.json`:**
   ```json
   {
     "crons": [{
       "path": "/api/scrape",
       "schedule": "0 9 * * *"
     }]
   }
   ```

3. **Deploy:**
   ```bash
   npm i -g vercel
   vercel --prod
   ```

---

## Option 4: GitHub Actions (Miễn phí)

### Ưu điểm:
- ✅ Hoàn toàn miễn phí
- ✅ Chạy từ GitHub
- ✅ 2000 phút/tháng free

### Setup:

1. **Tạo `.github/workflows/scrape.yml`:**
   ```yaml
   name: Daily TrendForce Scrape

   on:
     schedule:
       - cron: '0 9 * * *'  # 9 AM UTC daily
     workflow_dispatch:  # Cho phép chạy manual

   jobs:
     scrape:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v3

         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'

         - name: Install dependencies
           run: |
             pip install -r requirements.txt

         - name: Run scraper
           env:
             SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
             SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
           run: |
             python -c "from supabase_scraper import SupabaseScraper; s = SupabaseScraper(); s.scrape_and_save(1, 5)"
   ```

2. **Add secrets:**
   - Vào repo Settings → Secrets → Actions
   - Add `SUPABASE_URL` và `SUPABASE_KEY`

3. **Push và GitHub Actions sẽ chạy tự động!**

---

## Option 5: Heroku (Trả phí $7/tháng)

### Setup:

1. **Tạo `Procfile`:**
   ```
   worker: python supabase_scheduled.py
   ```

2. **Tạo `runtime.txt`:**
   ```
   python-3.11.0
   ```

3. **Deploy:**
   ```bash
   heroku create trendforce-scraper
   heroku config:set SUPABASE_URL=xxx
   heroku config:set SUPABASE_KEY=xxx
   git push heroku main
   heroku ps:scale worker=1
   ```

---

## Option 6: Google Cloud Run + Cloud Scheduler

### Ưu điểm:
- ✅ Free tier generous
- ✅ Serverless
- ✅ Highly scalable

### Setup:

1. **Tạo `Dockerfile`:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD python -c "from supabase_scraper import SupabaseScraper; s = SupabaseScraper(); s.scrape_and_save(1, 5)"
   ```

2. **Deploy:**
   ```bash
   gcloud run deploy trendforce-scraper \
     --source . \
     --region asia-southeast1 \
     --set-env-vars SUPABASE_URL=xxx,SUPABASE_KEY=xxx \
     --no-allow-unauthenticated
   ```

3. **Tạo Cloud Scheduler:**
   ```bash
   gcloud scheduler jobs create http scrape-daily \
     --schedule="0 9 * * *" \
     --uri="https://trendforce-scraper-xxx.run.app" \
     --http-method=POST
   ```

---

## Option 7: AWS Lambda + EventBridge

### Setup:

1. **Tạo Lambda function từ code**
2. **Package dependencies:**
   ```bash
   pip install -r requirements.txt -t .
   zip -r function.zip .
   ```
3. **Upload lên Lambda**
4. **Tạo EventBridge rule** chạy hàng ngày

---

## So sánh các options:

| Option | Cost | Ease | Best For |
|--------|------|------|----------|
| **Railway** | $5/mo | ⭐⭐⭐⭐⭐ | **Khuyến nghị** |
| **GitHub Actions** | Free | ⭐⭐⭐⭐ | Budget |
| Render | Free* | ⭐⭐⭐⭐ | Free tier |
| Vercel | Free | ⭐⭐⭐ | Serverless |
| Heroku | $7/mo | ⭐⭐⭐⭐ | Enterprise |
| GCP | Free* | ⭐⭐ | Scale |
| AWS | Pay-as-go | ⭐⭐ | AWS ecosystem |

---

## Khuyến nghị của tôi:

### 🥇 Best: GitHub Actions
- ✅ Hoàn toàn miễn phí
- ✅ Đơn giản
- ✅ Không cần quản lý server
- ✅ Perfect cho scheduled jobs

### 🥈 Alternative: Railway
- ✅ $5/tháng (affordable)
- ✅ Rất dễ dùng
- ✅ Chạy 24/7
- ✅ Có dashboard đẹp

### 🥉 Budget: Render
- ✅ Free tier
- ⚠️ Có giới hạn

---

## Monitoring & Logs

### Railway/Render/Heroku:
- Built-in logs trong dashboard
- View real-time

### GitHub Actions:
- Xem trong Actions tab
- Email notification nếu fail

### Vercel:
- Dashboard → Deployments → Logs

---

## Next Steps

1. Chọn platform phù hợp
2. Follow hướng dẫn setup ở trên
3. Set environment variables
4. Deploy!
5. Check logs để confirm chạy thành công

Sau khi deploy xong, bạn có thể:
- View data trong Supabase Dashboard
- Build frontend để hiển thị tin tức
- Tạo API endpoint để expose data
- Setup alerts khi có bài mới
