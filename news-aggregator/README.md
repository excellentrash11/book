# Economic News Aggregator

An automated daily news digest system designed for a YouTube series on economic news. This tool aggregates news from major sources, ranks stories by economic impact, analyzes market implications, and presents everything in a clean web interface.

## Features

- **Automated News Aggregation**: Pulls from 10+ major news sources via RSS feeds
- **Market Data Integration**: Tracks stocks, gold, treasury yields, forex, and macro indicators
- **AI-Powered Analysis**: Uses Claude to:
  - Rank stories by long-term US economic impact
  - Categorize stories (Cold Open, Macro Shift, Signal Check)
  - Extract key data points
  - Analyze market impact across asset classes
  - Generate compelling hooks
- **Daily Scheduling**: Automatic digest generation at 2pm PT
- **Web Interface**: Beautiful dashboard to view current and historical digests
- **Historical Archive**: Browse past digests anytime

## Quick Start

### 1. Get Your API Key

You'll need an Anthropic API key:
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Create an API key
4. Copy it (you'll need it soon)

### 2. Deploy to Railway (Easiest Method)

Railway is a free cloud platform that makes deployment simple:

1. **Create a Railway account**: Go to https://railway.app and sign up

2. **Deploy this project**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login to Railway
   railway login

   # Navigate to the project
   cd news-aggregator

   # Deploy
   railway up
   ```

3. **Set your API key**:
   - In Railway dashboard, go to your project
   - Click "Variables"
   - Add: `ANTHROPIC_API_KEY` with your API key

4. **Access your app**:
   - Railway will give you a URL (something like `your-app.railway.app`)
   - Visit it in your browser!

### 3. Alternative: Deploy to Render

Render is another free option:

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repo (or upload this code)
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash run.sh`
5. Add environment variable:
   - Key: `ANTHROPIC_API_KEY`
   - Value: Your API key
6. Click "Create Web Service"

### 4. Run Locally (For Development)

```bash
# Clone or download this project
cd news-aggregator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use any text editor

# Run the app
python app.py

# In another terminal, run the scheduler
python scheduler.py
```

Visit http://localhost:5000

## Configuration

Edit `.env` file to customize:

```env
# Required
ANTHROPIC_API_KEY=your_key_here

# Optional
TIMEZONE=America/Los_Angeles
DIGEST_TIME=14:00  # 2pm PT

# Optional: For additional market data
ALPHA_VANTAGE_API_KEY=your_key_here
```

## Usage

### Web Interface

- **Home**: View latest digest
- **History**: Browse all past digests
- **Generate**: Click button to manually generate a new digest

### Manual Generation

Generate a digest on-demand:

```bash
python -c "from app.digest_generator import DigestGenerator; import config; g = DigestGenerator(config.RSS_FEEDS, config.DATABASE_PATH, config.ANTHROPIC_API_KEY); print(g.generate_digest())"
```

## Understanding the Output

### Story Categories

- **Cold Open**: Absurd or destabilizing facts perfect for hooks
- **Macro Shift**: Major geopolitical or policy moves
- **Signal Check**: Smaller but notable stories to watch

### Market Impact Analysis

For each story, you'll see:
- **Key Data Points**: Important numbers, dates, companies
- **Market Impact**: How it affects:
  - Stocks (overall and by sector)
  - Bonds/Treasury yields
  - Dollar/Forex
  - Commodities (gold, oil)
- **Why It Matters**: Economic significance
- **Hook Potential**: Ideas for your cold open

## YouTube Series Structure

The digest is designed to map to your episode format:

1. **Cold Open** (1 min): Use stories tagged "cold_open" + their hook potential
2. **Macro Shift** (8-10 min): Deep dive on top "macro_shift" story
3. **Market Translation** (5-7 min): Use market impact analysis
4. **Signal Check** (2-3 min): Cover "signal_check" stories
5. **Close** (30 sec): Use "why it matters" insights

## Data Sources

### News Sources (Free)
- Reuters (Business, World)
- CNBC (Markets, Economics)
- MarketWatch
- Yahoo Finance
- WSJ (Economy, Markets)
- Federal Reserve Press Releases
- Treasury Press Releases
- BBC Business
- Financial Times

### Market Data (Free)
- **Yahoo Finance**: Stock indices, gold, forex
- **FRED API**: Fed funds rate, unemployment
- **Treasury.gov**: Bond yields

## Cost Estimate

- **News & Market Data**: 100% Free
- **Claude API**: ~$5-10/month
  - ~$0.50 per digest (4,000 tokens)
  - Daily = ~$15/month
  - But you control when it runs!

## Troubleshooting

### "No articles found"
- RSS feeds may be temporarily down
- Try again in a few minutes
- Check internet connection

### "AI analysis failed"
- Check your API key is correct
- Ensure you have API credits
- Check Anthropic status: https://status.anthropic.com

### Database errors
- Ensure `data/` directory exists
- Check file permissions

### Scheduling not working
- Verify timezone setting
- Check scheduler logs
- Ensure scheduler process is running

## Project Structure

```
news-aggregator/
├── app/
│   ├── news_aggregator.py    # RSS feed aggregation
│   ├── market_data.py         # Market data fetching
│   ├── ai_analyzer.py         # Claude-powered analysis
│   ├── database.py            # SQLite storage
│   └── digest_generator.py   # Orchestrates everything
├── templates/                 # Web interface HTML
├── data/                      # SQLite database
├── app.py                     # Flask web server
├── scheduler.py               # Daily scheduling
├── config.py                  # Configuration
└── requirements.txt           # Dependencies
```

## Development

### Adding News Sources

Edit `config.py`:

```python
RSS_FEEDS = [
    'https://your-source.com/rss',
    # ... add more
]
```

### Customizing Analysis

Edit prompts in `app/ai_analyzer.py` to adjust:
- Ranking criteria
- Category definitions
- Market analysis focus

### Changing Schedule

Edit `.env`:

```env
DIGEST_TIME=09:00  # 9am
TIMEZONE=America/New_York
```

## Support

- **Issues**: Report bugs or request features
- **Claude API**: https://docs.anthropic.com
- **Railway**: https://docs.railway.app
- **Render**: https://render.com/docs

## License

This project is for personal use. Respect API terms of service and rate limits.

## Tips for Your YouTube Series

1. **Preparation**: Review digest 1-2 hours before recording
2. **Research**: Click through to original articles for depth
3. **Visuals**: Use market data charts in your videos
4. **Updates**: Run manual generation right before recording for breaking news
5. **Archive**: Use history to spot trends over weeks/months

---

Built for analyzing economic news. Markets move fast - stay informed! 📊
