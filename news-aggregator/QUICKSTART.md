# Quick Start Guide

Get your Economic News Aggregator running in 5 minutes!

## Step 1: Get Your API Key (2 minutes)

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Click "Get API Keys"
4. Create a new key and copy it

💰 **Cost**: About $5-10/month for daily usage

## Step 2: Choose Your Deployment Method

### Option A: Deploy to Cloud (Recommended - No Technical Knowledge Required)

#### Railway (Easiest)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Add environment variable:
   - Name: `ANTHROPIC_API_KEY`
   - Value: [paste your API key]
6. Done! Railway will give you a URL

#### Render (Alternative)

1. Go to https://render.com
2. Sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `bash run.sh`
6. Add environment variable:
   - Key: `ANTHROPIC_API_KEY`
   - Value: [paste your API key]
7. Click "Create Web Service"

### Option B: Run on Your Computer

**Requirements**: Python 3.9 or higher

```bash
# 1. Download the project
cd news-aggregator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create configuration file
cp .env.example .env

# 4. Edit .env and add your API key
# Open .env in any text editor and paste your key

# 5. Run the web interface
python app.py
```

Open http://localhost:5000 in your browser!

**To enable automatic daily digests**, open a second terminal:

```bash
python scheduler.py
```

## Step 3: Generate Your First Digest

1. Open the web interface (the URL from Railway/Render, or http://localhost:5000)
2. Click the green "Generate New Digest" button
3. Wait 30-60 seconds
4. Browse your first digest!

## Step 4: Understanding Your Digest

Each digest shows:

### Market Snapshot
Current prices and changes for:
- Stock indices (S&P 500, Dow, NASDAQ)
- Gold prices
- Treasury yields
- Dollar strength

### Top 10 Stories
Ranked by economic impact, each story includes:

- **Category Badge**:
  - 🟡 Cold Open: Hook-worthy, surprising facts
  - 🔵 Macro Shift: Major policy/geopolitical moves
  - 🟢 Signal Check: Notable smaller stories

- **Importance Score**: 1-10 rating

- **Key Data Points**: Important numbers extracted from the story

- **Market Impact Analysis**: How this affects:
  - Stocks and specific sectors
  - Bonds and yields
  - Dollar and forex
  - Commodities (gold, oil)

- **Why It Matters**: Economic significance explained

- **Hook Potential**: Ideas for your video cold open

## Step 5: Using It for Your YouTube Series

### Daily Workflow

1. **Check digest at 2pm PT** (or whenever it's generated)
2. **Review top stories** - usually 1-2 will be your main focus
3. **Map to your structure**:
   - Cold Open: Use "hook potential" suggestions
   - Macro Shift: Deep dive on top macro_shift story
   - Market Translation: Reference the "market impact" sections
   - Signal Check: Cover 2-3 signal_check stories
   - Close: Use "why it matters" insights

### Pro Tips

- **Breaking News**: Click "Generate New Digest" anytime for fresh analysis
- **Historical Context**: Use History tab to see how stories developed over time
- **Data Points**: Screenshot the key data points for your video graphics
- **Market Snapshot**: Use for your market update segment

## Common Issues

### "No articles found"
- Wait a few minutes and try again
- RSS feeds may be temporarily down

### "AI analysis failed"
- Check your API key is correct
- Visit https://console.anthropic.com/ to check your credits
- Try again - temporary API issues happen

### Digest looks old
- Click "Generate New Digest" for fresh stories
- Scheduler runs automatically at 2pm PT

## Customization

### Change Digest Time

Edit `.env`:
```env
DIGEST_TIME=09:00  # Change to 9am
TIMEZONE=America/New_York  # Change timezone
```

### Add More News Sources

Edit `config.py` and add RSS feed URLs to `RSS_FEEDS` list

## Next Steps

- **Test it out**: Generate a few digests to get a feel for it
- **Adjust timing**: Set your preferred digest time
- **Bookmark the URL**: Add to your daily workflow
- **Check history**: Review past digests anytime

## Need Help?

- Check the full README.md for detailed documentation
- Claude API docs: https://docs.anthropic.com
- Railway docs: https://docs.railway.app
- Render docs: https://render.com/docs

---

You're all set! Generate your first digest and start creating amazing economic content. 📊🎥
