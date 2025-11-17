-- Thêm các columns tiếng Việt vào bảng trendforce_news
-- Chạy SQL này trong Supabase SQL Editor

ALTER TABLE trendforce_news
ADD COLUMN IF NOT EXISTS title_vi TEXT,
ADD COLUMN IF NOT EXISTS summary_vi TEXT,
ADD COLUMN IF NOT EXISTS translated_at TIMESTAMP WITH TIME ZONE;

-- Tạo index cho tìm kiếm tiếng Việt
CREATE INDEX IF NOT EXISTS idx_trendforce_news_title_vi
ON trendforce_news USING gin(to_tsvector('simple', title_vi));

-- Comment
COMMENT ON COLUMN trendforce_news.title_vi IS 'Tiêu đề bài viết bằng tiếng Việt';
COMMENT ON COLUMN trendforce_news.summary_vi IS 'Tóm tắt bằng tiếng Việt';
COMMENT ON COLUMN trendforce_news.translated_at IS 'Thời gian được dịch';
