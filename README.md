# TrendForce News Aggregator 🚀

> Full-stack news aggregation system for semiconductor & tech industry. Scrape, store, translate, and visualize news from multiple sources with a beautiful web interface.

[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel)](https://vercel.com)
[![Supabase](https://img.shields.io/badge/Database-Supabase-green?logo=supabase)](https://supabase.com)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)](https://python.org)
[![Tailwind CSS](https://img.shields.io/badge/Styled%20with-Tailwind%20CSS-38B2AC?logo=tailwind-css)](https://tailwindcss.com)

**Live Demo**: [Coming soon after deployment]

---

## ✨ Features

### 📰 Multi-Source Scraping
- **TrendForce News** - Latest industry news
- **TrendForce Press Center** - Press releases & announcements
- Automatic duplicate detection
- Scheduled daily scraping (10 PM Vietnam time)

### 🌐 Beautiful Web Interface
- **Filter by source**: All / News / Press Release
- **Search**: Real-time across titles and summaries
- **Sort**: Newest/Oldest/Title A-Z
- **Responsive**: Mobile, tablet, desktop
- **Source badges**: Visual distinction between News and Press Release
- **Vietnamese badge**: Shows which articles have translations

### 🇻🇳 Multilingual Support
- Schema ready for Vietnamese translations
- Prepared for n8n + AI translation workflow
- Automatic fallback: Vietnamese → English

### 📊 Statistics Dashboard
- Total articles count
- Today's new articles
- This week's articles
- Source breakdown

### 🔧 Developer-Friendly
- Clean, organized codebase
- Comprehensive documentation
- Easy deployment (Vercel + GitHub Actions)
- Environment-based configuration

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Git
- Supabase account (free tier works)
- Vercel account (optional, for deployment)

### 1. Clone & Install

```bash
git clone https://github.com/duongthien408-create/rss-custom.git
cd rss-custom
pip install -r requirements.txt
```

### 2. Setup Database

1. Create a Supabase project at https://supabase.com
2. Run SQL migrations in order:
   ```sql
   -- 1. Create main table
   sql/create_supabase_table.sql

   -- 2. Add Vietnamese columns
   sql/add_vietnamese_columns.sql

   -- 3. Add article_id and source columns
   sql/add_article_id_column.sql
   ```
3. Get your API credentials from Settings → API

### 3. Configure Environment

Create `.env` file:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### 4. Run Scrapers

```bash
# Scrape News only
python scripts/trendforce_scraper.py

# Scrape Press Center only
python scripts/presscenter_scraper.py

# Scrape everything (recommended)
python scripts/combined_scraper.py
```

### 5. View Results

Open `public/index.html` in your browser, or deploy to Vercel for live hosting.

---

## 📁 Project Structure

```
rss-custom/
├── .github/workflows/     # GitHub Actions for scheduled scraping
├── api/                   # Vercel serverless functions
│   └── scrape.py         # API endpoint for cron jobs
├── archive/              # Old test files & outputs
├── docs/                 # Documentation & guides
│   ├── DEPLOYMENT.md
│   ├── SCHEDULE_GUIDE.md
│   ├── SUPABASE_SETUP.md
│   └── VERCEL_DEPLOY.md
├── public/               # Frontend (static site)
│   ├── index.html        # Main UI
│   └── app.js            # JavaScript logic
├── scripts/              # Python scrapers
│   ├── trendforce_scraper.py      # News scraper
│   ├── presscenter_scraper.py     # Press Center scraper
│   ├── combined_scraper.py        # Combined (main)
│   └── supabase_scraper.py        # Legacy version
├── sql/                  # Database migrations
│   ├── create_supabase_table.sql
│   ├── add_vietnamese_columns.sql
│   └── add_article_id_column.sql
├── .env                  # Environment variables (create this)
├── .env.example          # Example env file
├── .gitignore
├── CHANGELOG.md          # What we've built
├── README.md             # You are here
├── ROADMAP.md            # Future plans
├── requirements.txt      # Python dependencies
└── vercel.json           # Vercel deployment config
```

---

## 🎯 Usage Examples

### Python API

```python
from scripts.trendforce_scraper import TrendForceScraper

# Initialize
scraper = TrendForceScraper()

# Scrape one page
articles = scraper.scrape_page(1)

# Scrape multiple pages with delay
all_articles = scraper.scrape_multiple_pages(
    start_page=1,
    end_page=3,
    delay=1.5  # seconds
)

# Save to files
scraper.save_to_json(all_articles, 'output.json')
scraper.save_to_csv(all_articles, 'output.csv')
```

### Combined Scraper (Recommended)

```bash
python scripts/combined_scraper.py
```

This will:
1. Scrape 3 pages from News
2. Scrape 2 pages from Press Center
3. Check for duplicates
4. Insert new articles into Supabase
5. Show summary statistics

---

## 🔄 Automation & Scheduling

### Option 1: Vercel Cron (Recommended for production)

Already configured in `vercel.json`:
```json
{
  "crons": [{
    "path": "/api/scrape",
    "schedule": "0 15 * * *"  // 10 PM Vietnam time
  }]
}
```

**Note**: Requires Vercel Pro ($20/month) for cron jobs.

### Option 2: GitHub Actions (Free)

Already configured in `.github/workflows/scrape.yml`:
- Runs daily at 10 PM Vietnam time
- Uses GitHub Secrets for credentials
- Free tier: 2000 minutes/month

**Setup**:
1. Add secrets to your GitHub repo:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
2. Enable GitHub Actions
3. Done! Will run automatically

### Option 3: Manual cron (Self-hosted)

```bash
# Linux/Mac crontab
0 22 * * * cd /path/to/project && python scripts/combined_scraper.py

# Windows Task Scheduler
# Use archive/run_scraper.bat
```

---

## 🌍 Deployment

### Deploy to Vercel

1. **Via CLI**:
   ```bash
   npm i -g vercel
   vercel
   ```

2. **Via GitHub**:
   - Push to GitHub
   - Import repo in Vercel dashboard
   - Add environment variables
   - Deploy!

3. **Environment Variables** (Vercel Dashboard):
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

See [docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md) for details.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.7+ |
| **Scraping** | BeautifulSoup4, Requests |
| **Database** | Supabase (PostgreSQL) |
| **Frontend** | HTML5, Vanilla JavaScript |
| **Styling** | Tailwind CSS |
| **Deployment** | Vercel (Static + Serverless) |
| **CI/CD** | GitHub Actions |
| **Scheduling** | Vercel Cron / GitHub Actions |
| **Future** | n8n (translation), OpenAI API |

---

## 📚 Documentation

- **[CHANGELOG.md](CHANGELOG.md)** - What we've built today
- **[ROADMAP.md](ROADMAP.md)** - Future plans & ideas
- **[docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md)** - Database setup guide
- **[docs/VERCEL_DEPLOY.md](docs/VERCEL_DEPLOY.md)** - Deployment guide
- **[docs/SCHEDULE_GUIDE.md](docs/SCHEDULE_GUIDE.md)** - Scheduling options

---

## 🇻🇳 Vietnamese Translation (Planned)

### Current State
- Database schema ready (title_vi, summary_vi, translated_at)
- UI displays Vietnamese when available
- Badge shows translation status

### Coming Soon
Auto-translation workflow:
1. New article scraped → Supabase
2. Supabase webhook → n8n
3. n8n → OpenAI/Claude API
4. Translated content → Update Supabase
5. 🇻🇳 Badge appears on UI

**Estimated cost**: ~$0.01-0.03 per article

---

## 📊 Database Schema

```sql
CREATE TABLE trendforce_news (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT UNIQUE NOT NULL,
  date DATE,
  category TEXT,
  summary TEXT,
  thumbnail TEXT,

  -- Vietnamese translation
  title_vi TEXT,
  summary_vi TEXT,
  translated_at TIMESTAMP,

  -- Metadata
  article_id TEXT,
  source TEXT DEFAULT 'news',  -- 'news' or 'presscenter'
  scraped_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🤝 Contributing

Contributions welcome! See [ROADMAP.md](ROADMAP.md) for ideas.

### Priority Features
1. More news sources (AnandTech, Tom's Hardware, etc.)
2. AI Vietnamese translation via n8n
3. Full article content extraction
4. RSS feed generation
5. Email digest

---

## 📄 License

MIT License - feel free to use for personal or commercial projects.

---

## 🙏 Credits

- **Data Source**: [TrendForce](https://www.trendforce.com)
- **Database**: [Supabase](https://supabase.com)
- **Hosting**: [Vercel](https://vercel.com)
- **Developer**: Built with [Claude Code](https://claude.com/claude-code)

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/duongthien408-create/rss-custom/issues)
- **Owner**: [@duongthien408-create](https://github.com/duongthien408-create)

---

## 🎉 Quick Links

- [Live Demo](#) (coming soon)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Supabase Dashboard](https://supabase.com/dashboard)
- [Vercel Dashboard](https://vercel.com/dashboard)

---

**Star ⭐ this repo if you found it helpful!**

Last updated: 2025-11-18
