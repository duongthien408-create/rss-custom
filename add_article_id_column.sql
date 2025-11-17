-- Thêm columns article_id và source vào bảng trendforce_news
-- Chạy SQL này trong Supabase SQL Editor

ALTER TABLE trendforce_news
ADD COLUMN IF NOT EXISTS article_id TEXT,
ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'news';

-- Tạo index cho article_id để tìm kiếm nhanh
CREATE INDEX IF NOT EXISTS idx_trendforce_news_article_id
ON trendforce_news(article_id);

-- Tạo index cho source để filter theo nguồn
CREATE INDEX IF NOT EXISTS idx_trendforce_news_source
ON trendforce_news(source);

-- Comments
COMMENT ON COLUMN trendforce_news.article_id IS 'ID của bài viết được extract từ URL';
COMMENT ON COLUMN trendforce_news.source IS 'Nguồn bài viết: news hoặc presscenter';
