# Hướng dẫn nhanh: Thiết lập chạy tự động hàng ngày

## Cách đơn giản nhất - Windows Task Scheduler

### Bước 1: Test thử bằng tay

Double-click file `run_once.bat`

Nếu chạy thành công, bạn sẽ thấy file mới được tạo với tên kiểu `trendforce_daily_20251117.json`

### Bước 2: Mở Task Scheduler

1. Nhấn phím `Windows` + `R`
2. Gõ: `taskschd.msc`
3. Nhấn Enter

### Bước 3: Tạo Task mới

1. Trong Task Scheduler, click **"Create Basic Task..."** ở menu bên phải
2. Điền thông tin:

   **Tên task:** `TrendForce Daily Scraper`

   **Description:** `Scrape tin tức TrendForce mỗi ngày lúc 9:00 sáng`

3. Click **Next**

### Bước 4: Chọn lịch chạy

1. Chọn **"Daily"**
2. Click **Next**
3. Chọn thời gian bắt đầu: **9:00:00 AM**
4. Recur every: **1 days**
5. Click **Next**

### Bước 5: Chọn hành động

1. Chọn **"Start a program"**
2. Click **Next**
3. Click **Browse...**
4. Tìm đến file: `run_once.bat` trong folder này
5. Click **Next**

### Bước 6: Hoàn thành

1. Review lại thông tin
2. Click **Finish**

---

## Kiểm tra Task hoạt động

### Cách 1: Chạy thử ngay

1. Trong Task Scheduler, tìm task "TrendForce Daily Scraper"
2. Right-click → **Run**
3. Kiểm tra folder này, sẽ có file mới `trendforce_daily_YYYYMMDD.json`

### Cách 2: Xem lịch sử

1. Click vào task
2. Tab **History** ở dưới cùng
3. Xem các lần chạy và kết quả

---

## Tùy chỉnh nâng cao

### Thay đổi giờ chạy

1. Right-click task → **Properties**
2. Tab **Triggers**
3. Double-click trigger
4. Sửa thời gian
5. OK

### Chạy ngay cả khi không đăng nhập

1. Right-click task → **Properties**
2. Tab **General**
3. Chọn **"Run whether user is logged on or not"**
4. OK (có thể phải nhập password)

### Chạy lại nếu miss schedule

1. Right-click task → **Properties**
2. Tab **Settings**
3. Check **"Run task as soon as possible after a scheduled start is missed"**
4. OK

---

## Các file output

Mỗi ngày, script sẽ tạo 2 file:

- `trendforce_daily_20251117.json` - Định dạng JSON
- `trendforce_daily_20251117.csv` - Định dạng CSV

Tên file có ngày tháng để dễ phân biệt từng lần chạy.

---

## Troubleshooting

### Task không chạy?

**Kiểm tra 1:** Python có trong PATH không?
```
Mở CMD, gõ: python --version
```

**Kiểm tra 2:** Chạy thử `run_once.bat` bằng tay
```
Double-click run_once.bat
```

**Kiểm tra 3:** Xem Task History để tìm lỗi

### Task chạy nhưng không có file output?

Kiểm tra "Start in" directory trong task properties phải trỏ đúng folder.

---

## Cách khác: Dùng Python Schedule

Nếu không muốn dùng Task Scheduler:

```bash
pip install schedule
python scheduled_scraper.py
```

Script sẽ chạy liên tục và tự động scrape mỗi ngày lúc 9:00 AM.

**Lưu ý:** Script phải chạy liên tục (giống như để một chương trình mở).
