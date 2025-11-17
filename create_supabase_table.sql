-- SQL script để tạo bảng trong Supabase
-- Copy và chạy trong Supabase SQL Editor

-- Tạo bảng trendforce_news
CREATE TABLE IF NOT EXISTS trendforce_news (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    date TEXT,
    category TEXT,
    summary TEXT,
    thumbnail TEXT,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tạo index để tăng tốc độ query
CREATE INDEX IF NOT EXISTS idx_trendforce_news_date ON trendforce_news(date DESC);
CREATE INDEX IF NOT EXISTS idx_trendforce_news_url ON trendforce_news(url);
CREATE INDEX IF NOT EXISTS idx_trendforce_news_title ON trendforce_news USING gin(to_tsvector('english', title));

-- Enable Row Level Security (RLS) - tùy chọn
ALTER TABLE trendforce_news ENABLE ROW LEVEL SECURITY;

-- Tạo policy cho phép read public (nếu muốn)
CREATE POLICY "Allow public read access" ON trendforce_news
    FOR SELECT
    USING (true);

-- Tạo policy cho phép insert với service key
CREATE POLICY "Allow authenticated insert" ON trendforce_news
    FOR INSERT
    WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- Comment
COMMENT ON TABLE trendforce_news IS 'Bảng lưu tin tức từ TrendForce';
COMMENT ON COLUMN trendforce_news.title IS 'Tiêu đề bài viết';
COMMENT ON COLUMN trendforce_news.url IS 'URL bài viết (unique)';
COMMENT ON COLUMN trendforce_news.date IS 'Ngày đăng bài';
COMMENT ON COLUMN trendforce_news.category IS 'Danh mục';
COMMENT ON COLUMN trendforce_news.summary IS 'Tóm tắt nội dung';
COMMENT ON COLUMN trendforce_news.thumbnail IS 'Link hình thumbnail';
COMMENT ON COLUMN trendforce_news.scraped_at IS 'Thời gian scrape';
COMMENT ON COLUMN trendforce_news.created_at IS 'Thời gian tạo record';
