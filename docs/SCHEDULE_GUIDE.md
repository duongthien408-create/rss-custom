# Hướng dẫn chạy TrendForce Scraper theo lịch

## Có 3 cách chạy tự động hàng ngày:

---

## Cách 1: Sử dụng Python Schedule (Khuyến nghị cho testing)

### Bước 1: Cài đặt thư viện schedule

```bash
pip install schedule
```

### Bước 2: Chạy script scheduler

```bash
python scheduled_scraper.py
```

Script sẽ:
- Chạy ngay lần đầu tiên
- Sau đó chạy lại mỗi ngày lúc 09:00 sáng
- Lưu file với tên có timestamp: `trendforce_daily_YYYYMMDD.json`

**Lưu ý:** Script này phải chạy liên tục (không tắt). Nhấn Ctrl+C để dừng.

---

## Cách 2: Windows Task Scheduler (Khuyến nghị cho production)

### Bước 1: Mở Task Scheduler

1. Nhấn `Win + R`
2. Gõ `taskschd.msc` và Enter

### Bước 2: Tạo Task mới

1. Click "Create Basic Task"
2. Đặt tên: "TrendForce Daily Scraper"
3. Chọn "Daily"
4. Chọn thời gian chạy (ví dụ: 09:00 AM)
5. Chọn "Start a program"
6. Browse đến file: `run_once.bat`
7. Finish

### Bước 3: Cấu hình nâng cao (Optional)

1. Right-click task vừa tạo → Properties
2. Tab "General": Check "Run whether user is logged on or not"
3. Tab "Conditions": Uncheck "Start the task only if the computer is on AC power"
4. Tab "Settings": Check "Run task as soon as possible after a scheduled start is missed"

**Kết quả:** Task Scheduler sẽ tự động chạy `run_once.bat` mỗi ngày lúc 09:00 AM

---

## Cách 3: Sử dụng Cron (Linux/Mac) hoặc WSL

### Bước 1: Tạo shell script

```bash
#!/bin/bash
cd "c:/Users/duong/Documents/trend forces rss"
python -c "from scheduled_scraper import run_daily_scrape; run_daily_scrape()"
```

Lưu file này là `run_scraper.sh` và chmod:

```bash
chmod +x run_scraper.sh
```

### Bước 2: Thêm vào crontab

```bash
crontab -e
```

Thêm dòng này (chạy lúc 9:00 AM mỗi ngày):

```
0 9 * * * /path/to/run_scraper.sh
```

---

## Cách 4: Chạy bằng tay khi cần

Đơn giản chạy:

```bash
python example_usage.py
```

Hoặc double-click file `run_once.bat`

---

## Tùy chỉnh thời gian và số trang

Mở file [scheduled_scraper.py](scheduled_scraper.py) và sửa:

### Thay đổi thời gian chạy:

```python
# Thay đổi từ 09:00 sang 14:30
schedule.every().day.at("14:30").do(run_daily_scrape)

# Hoặc chạy mỗi 6 giờ
schedule.every(6).hours.do(run_daily_scrape)

# Hoặc chạy mỗi thứ 2
schedule.every().monday.at("09:00").do(run_daily_scrape)
```

### Thay đổi số trang scrape:

```python
# Trong hàm run_daily_scrape(), sửa dòng này:
articles = scraper.scrape_multiple_pages(
    start_page=1,
    end_page=10,  # Thay đổi từ 3 sang 10 để scrape 10 trang
    delay=1.5
)
```

---

## Kiểm tra logs

Mỗi lần chạy, script sẽ in ra:
- Thời gian bắt đầu
- Số bài viết đã scrape
- Tên file đã lưu
- Thời gian scrape tiếp theo

Nếu dùng Task Scheduler, logs sẽ xuất hiện trong Task Scheduler History.

---

## Troubleshooting

### Task Scheduler không chạy?

1. Kiểm tra path đến Python có đúng không
2. Chạy thử `run_once.bat` bằng tay để kiểm tra lỗi
3. Kiểm tra Task History trong Task Scheduler

### Script bị lỗi?

Chạy thử bằng tay:

```bash
python scheduled_scraper.py
```

Và xem lỗi hiện ra.

---

## So sánh các phương pháp

| Phương pháp | Ưu điểm | Nhược điểm | Khuyến nghị |
|-------------|---------|------------|-------------|
| Python Schedule | Dễ setup, flexible | Phải chạy liên tục | Testing |
| Task Scheduler | Tự động, không cần chạy script liên tục | Chỉ Windows | **Production (Windows)** |
| Cron | Tự động, tiêu chuẩn Unix | Chỉ Linux/Mac | Production (Linux/Mac) |
| Manual | Linh hoạt | Phải nhớ chạy | Ad-hoc |
