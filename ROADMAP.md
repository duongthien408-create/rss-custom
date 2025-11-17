# Roadmap - TrendForce News Aggregator

## Mục tiêu tổng quan
Xây dựng hệ thống tổng hợp tin tức công nghệ toàn diện, đa nguồn, đa ngôn ngữ với khả năng phân tích và cá nhân hóa nội dung.

---

## Phase 1: Foundation ✅ HOÀN THÀNH
**Timeline**: Đã hoàn thành (2025-11-18)

### ✅ Completed
- [x] Scraper cho TrendForce News
- [x] Scraper cho TrendForce Press Center
- [x] Combined scraper (multi-source)
- [x] Supabase database setup
- [x] Vietnamese translation support (schema)
- [x] Web UI với Tailwind CSS
- [x] Source filtering (News/Press Release)
- [x] Vercel deployment
- [x] GitHub Actions scheduling
- [x] Documentation

---

## Phase 2: Multi-Source Expansion 🚀

### Thêm nguồn tin chất lượng từ TrendForce

#### 2.1 TrendForce Insights
**URL**: https://www.trendforce.com/insights
**Priority**: HIGH

**Tại sao quan trọng**:
- Bài phân tích chuyên sâu hơn News
- Industry reports, market forecasts
- Paid content preview (tóm tắt free)

**Technical approach**:
- Tạo `scripts/insights_scraper.py`
- Parse structure: Title, Author, Date, Summary, Category tags
- Thêm field `content_type`: 'news', 'presscenter', 'insights'
- Filter UI: thêm tab "📊 Insights"

**Estimated effort**: 4-6 hours

---

#### 2.2 TrendForce Research
**URL**: https://www.trendforce.com/research
**Priority**: MEDIUM

**Nội dung**:
- Market research reports
- Quarterly forecasts
- Industry analysis

**Challenge**:
- Có thể bị paywall
- Cần scrape metadata + preview text
- Link đến full reports (external)

**Estimated effort**: 6-8 hours

---

#### 2.3 Các nguồn bên ngoài khác

**Danh sách đề xuất**:

1. **AnandTech** - https://www.anandtech.com/
   - CPU, GPU, storage reviews
   - Highly technical content
   - RSS feed available

2. **Tom's Hardware** - https://www.tomshardware.com/
   - Hardware news & reviews
   - Benchmark data
   - RSS feed available

3. **SemiWiki** - https://semiwiki.com/
   - Semiconductor industry news
   - Technical deep-dives
   - Community-driven

4. **EE Times** - https://www.eetimes.com/
   - Electronics industry news
   - IoT, AI, automotive
   - Professional audience

5. **Semiconductor Digest** - https://www.semiconductor-digest.com/
   - Chip industry news
   - Manufacturing updates

**Implementation approach**:
- Tạo base class `BaseScraper` để các scraper kế thừa
- Mỗi nguồn có config riêng (URL patterns, selectors)
- Thêm column `source_domain` để phân biệt (trendforce.com, anandtech.com, etc.)
- UI: Dropdown filter "All Sources" / "TrendForce" / "AnandTech" / etc.

**Estimated effort**: 2-3 days (for 3-4 sources)

---

## Phase 3: Content Enhancement 📝

### 3.1 Full Article Content Extraction
**Current**: Chỉ lưu title + summary
**Goal**: Scrape full article text

**Benefits**:
- Full-text search
- Better AI summarization
- Offline reading
- Archive capability

**Technical**:
- Tạo `scripts/full_content_scraper.py`
- Thêm column `content_full TEXT` vào DB
- Parse HTML → Markdown
- Handle images, code blocks, tables
- Respect robots.txt

**Challenges**:
- Dynamic content (JavaScript-rendered)
- Paywalls
- Large DB size

**Solutions**:
- Sử dụng Playwright/Selenium cho JS sites
- Chỉ scrape preview cho paywalled content
- Compress/summarize old articles

**Estimated effort**: 1 week

---

### 3.2 AI-Powered Vietnamese Translation
**Current**: Schema sẵn sàng, chưa có workflow
**Goal**: Tự động dịch mọi bài viết sang tiếng Việt

**Workflow**:
```
New Article Scraped
  ↓
Webhook/Cron trigger n8n
  ↓
n8n calls OpenAI/Claude API
  ↓
Translate title + summary
  ↓
Update Supabase (title_vi, summary_vi)
  ↓
Badge 🇻🇳 hiện lên UI
```

**Tech stack**:
- **n8n**: Workflow automation (self-hosted hoặc cloud)
- **AI API**: OpenAI GPT-4 hoặc Claude 3
- **Supabase webhook**: Trigger on new insert
- **Rate limiting**: Avoid API overuse

**Cost estimate**:
- OpenAI GPT-4: ~$0.01-0.03 per article
- Claude 3: ~$0.01-0.02 per article
- n8n: Free (self-hosted) hoặc $20/month (cloud)

**Estimated effort**: 2-3 days

---

### 3.3 AI Summarization & Key Points
**Goal**: Tự động tạo tóm tắt ngắn gọn + bullet points

**Features**:
- **TL;DR**: 1-2 câu tóm tắt
- **Key points**: 3-5 bullet points
- **Tags**: Auto-generate tags (AI, 5G, TSMC, etc.)
- **Sentiment**: Positive/Negative/Neutral
- **Reading time**: Estimate

**DB Schema**:
```sql
ALTER TABLE trendforce_news ADD COLUMN tldr TEXT;
ALTER TABLE trendforce_news ADD COLUMN key_points TEXT[]; -- array
ALTER TABLE trendforce_news ADD COLUMN tags TEXT[];
ALTER TABLE trendforce_news ADD COLUMN sentiment VARCHAR(20);
ALTER TABLE trendforce_news ADD COLUMN reading_time_minutes INT;
```

**UI Enhancement**:
- Hiển thị tags dưới dạng badges
- "Key Points" collapsible section
- Sentiment icon (👍/👎/😐)

**Estimated effort**: 1 week

---

## Phase 4: Advanced Features 🔥

### 4.1 RSS Feed Generation
**Goal**: Tạo RSS feed cho users subscribe

**Endpoints**:
- `/rss/all.xml` - Tất cả bài viết
- `/rss/news.xml` - Chỉ News
- `/rss/press.xml` - Chỉ Press Release
- `/rss/insights.xml` - Chỉ Insights
- `/rss/vi.xml` - Chỉ bài đã dịch tiếng Việt

**Tech**:
- Python `feedgen` library
- Vercel serverless function `/api/rss/[type].py`
- Cache 15 minutes

**Estimated effort**: 4-6 hours

---

### 4.2 Email Digest
**Goal**: Gửi email tóm tắt hàng ngày/tuần

**Features**:
- Daily digest: Top 5 bài mới nhất
- Weekly digest: Top 10 bài hot nhất
- Personalized: Theo tags user quan tâm
- Beautiful HTML email template

**Tech stack**:
- **Email service**: SendGrid / Mailgun / Resend
- **Scheduler**: Vercel Cron + Supabase Functions
- **Subscriber management**: Supabase table `subscribers`

**Workflow**:
```
Cron trigger (daily 6 AM)
  ↓
Query top articles from Supabase
  ↓
Generate HTML email
  ↓
Send to all subscribers
  ↓
Log delivery status
```

**Estimated effort**: 1 week

---

### 4.3 Search Engine
**Goal**: Full-text search với autocomplete

**Features**:
- Real-time search as you type
- Search across: title, summary, content, tags
- Filters: Date range, source, language
- Autocomplete suggestions
- Search history

**Tech**:
- **Backend**: Supabase full-text search (PostgreSQL GIN index)
- **Frontend**: Algolia-like UI
- **Caching**: Redis for autocomplete

**SQL Setup**:
```sql
-- Full-text search index
CREATE INDEX idx_fulltext_search ON trendforce_news
USING gin(
  to_tsvector('english', title || ' ' || summary || ' ' || content_full)
);
```

**Estimated effort**: 3-4 days

---

### 4.4 User Accounts & Personalization
**Goal**: Cho phép users tạo tài khoản và customize feed

**Features**:
- User registration/login (Supabase Auth)
- Bookmark articles
- Follow tags (AI, TSMC, Memory, etc.)
- Hide/show sources
- Reading history
- Personalized recommendations

**DB Schema**:
```sql
CREATE TABLE bookmarks (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users,
  article_id INT REFERENCES trendforce_news,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_tags (
  id SERIAL PRIMARY KEY,
  user_id UUID REFERENCES auth.users,
  tag VARCHAR(50),
  UNIQUE(user_id, tag)
);
```

**Estimated effort**: 2 weeks

---

## Phase 5: Analytics & Insights 📊

### 5.1 Trending Topics
**Goal**: Phát hiện chủ đề đang hot

**Approach**:
- Extract keywords từ articles (NLP/AI)
- Count frequency theo timeframe
- Hiển thị word cloud / trending list
- "Hot Topics" sidebar widget

**Tech**:
- Python `spaCy` hoặc `transformers` (BERT)
- PostgreSQL aggregation queries
- Chart.js for visualization

**Estimated effort**: 1 week

---

### 5.2 Article Similarity & Recommendations
**Goal**: "You might also like" feature

**Approach**:
- Embedding vectors (OpenAI Embeddings hoặc SentenceTransformers)
- Store trong Supabase `pgvector` extension
- Cosine similarity search
- Recommend 3-5 related articles

**Tech**:
```sql
-- Install pgvector extension
CREATE EXTENSION vector;

ALTER TABLE trendforce_news ADD COLUMN embedding vector(1536);

-- Similarity search
SELECT * FROM trendforce_news
ORDER BY embedding <-> '[your_query_embedding]'
LIMIT 5;
```

**Estimated effort**: 1 week

---

### 5.3 Dashboard & Statistics
**Goal**: Admin dashboard để xem stats

**Metrics**:
- Articles scraped per day
- Sources breakdown
- Top tags
- Translation coverage (% bài đã dịch)
- User activity (if user accounts enabled)
- API usage

**Tech**:
- Separate admin page `/admin`
- Charts: Chart.js / Recharts
- Auth: Supabase RLS + admin role

**Estimated effort**: 3-4 days

---

## Phase 6: Mobile & PWA 📱

### 6.1 Progressive Web App
**Goal**: Cài đặt như native app

**Features**:
- Offline reading (Service Worker cache)
- Push notifications (new articles)
- App manifest
- Fast loading (< 2s)

**Tech**:
- Service Worker registration
- IndexedDB for offline data
- Web Push API
- Lighthouse score > 90

**Estimated effort**: 1 week

---

### 6.2 Mobile App (Optional)
**Goal**: Native iOS/Android app

**Options**:
- **React Native**: Share codebase
- **Flutter**: Better performance
- **Capacitor**: Wrap existing web app

**Features**:
- Same as PWA
- Better UX
- Native share
- Biometric login

**Estimated effort**: 1-2 months (for both platforms)

---

## Technical Debt & Improvements

### Code Quality
- [ ] Add unit tests (pytest)
- [ ] Add integration tests
- [ ] Type hints (Python typing)
- [ ] ESLint + Prettier for JS
- [ ] Pre-commit hooks
- [ ] CI/CD pipeline for tests

### Performance
- [ ] Database query optimization
- [ ] Add Redis caching layer
- [ ] CDN for images (Cloudinary/imgix)
- [ ] Lazy loading images
- [ ] Infinite scroll instead of pagination
- [ ] Compress responses (gzip)

### Security
- [ ] API rate limiting
- [ ] CORS configuration
- [ ] Input validation
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention
- [ ] HTTPS only
- [ ] Environment variable validation

### Monitoring
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (Vercel Analytics)
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Log aggregation (Logtail/Papertrail)

---

## Long-term Vision

### Year 1
- Scrape từ 10+ nguồn uy tín
- 1000+ articles in database
- Full Vietnamese translation
- Email digest với 100+ subscribers
- PWA deployment

### Year 2
- AI-powered personalization
- Mobile apps (iOS/Android)
- Community features (comments, discussions)
- Premium features (exclusive content, advanced search)
- API for third-party developers

### Year 3
- Expand sang các industry khác (automotive, IoT, AI/ML)
- Multilingual support (Tiếng Việt, English, Chinese, Japanese)
- Video/podcast content aggregation
- Marketplace for premium research reports

---

## Prioritization Matrix

| Feature | Impact | Effort | Priority |
|---------|--------|--------|----------|
| Multi-source scraping | HIGH | MEDIUM | 🔥 P0 |
| AI Vietnamese translation | HIGH | LOW | 🔥 P0 |
| Full article content | MEDIUM | HIGH | P1 |
| RSS feeds | MEDIUM | LOW | P1 |
| Email digest | MEDIUM | MEDIUM | P1 |
| Search engine | HIGH | MEDIUM | P1 |
| User accounts | HIGH | HIGH | P2 |
| Trending topics | MEDIUM | MEDIUM | P2 |
| PWA | MEDIUM | MEDIUM | P2 |
| Mobile apps | LOW | VERY HIGH | P3 |

**P0**: Ship ASAP (next sprint)
**P1**: Next quarter
**P2**: This year
**P3**: Long-term / Nice-to-have

---

## Estimated Timeline

### Sprint 1 (Week 1-2): Multi-Source
- AnandTech scraper
- Tom's Hardware scraper
- UI: Source dropdown filter
- Testing & debugging

### Sprint 2 (Week 3-4): AI Translation
- n8n workflow setup
- OpenAI/Claude integration
- Batch translate existing articles
- Monitor translation quality

### Sprint 3 (Week 5-6): Content Enhancement
- Full article scraper
- AI summarization (TL;DR, key points)
- Tags generation
- UI updates

### Sprint 4 (Week 7-8): RSS & Email
- RSS feed generation
- Email template design
- Subscriber system
- SendGrid integration

### Sprint 5 (Week 9-10): Search & Discovery
- Full-text search implementation
- Autocomplete
- Related articles (similarity)
- Trending topics

### Sprint 6 (Week 11-12): Polish & Launch
- Performance optimization
- Bug fixes
- Documentation
- Marketing (ProductHunt, Reddit)

---

## Success Metrics

### Technical KPIs
- Uptime: > 99.5%
- Page load time: < 2s
- API response time: < 500ms
- Scraper success rate: > 95%
- Translation coverage: > 80%

### Product KPIs
- Monthly Active Users: 1000+
- Articles scraped per day: 50+
- Email subscribers: 100+
- Avg session duration: > 5 min
- Return visitor rate: > 40%

---

## Resources Needed

### Services
- **Vercel Pro**: $20/month (more cron jobs)
- **Supabase Pro**: $25/month (more DB storage)
- **OpenAI API**: ~$50/month (translation)
- **SendGrid**: Free tier (12k emails/month)
- **Domain**: $12/year

**Total**: ~$100/month

### Time Investment
- **Phase 2-3**: 1-2 months (part-time)
- **Phase 4-5**: 2-3 months (part-time)
- **Phase 6**: 1-2 months (full-time)

---

## Community & Open Source

### Potential Contributors
- Frontend devs (React/Vue enthusiasts)
- Data scientists (NLP, ML)
- Designers (UI/UX improvements)
- Translators (proofreading AI translations)

### Open Source Strategy
- MIT License
- Contribution guidelines
- Good first issues tagged
- Monthly community calls

---

**Last Updated**: 2025-11-18
**Next Review**: 2025-12-01

