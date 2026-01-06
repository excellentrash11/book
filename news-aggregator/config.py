import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')

# Scheduling
TIMEZONE = os.getenv('TIMEZONE', 'America/Los_Angeles')
DIGEST_TIME = os.getenv('DIGEST_TIME', '14:00')

# RSS Feed Sources
RSS_FEEDS = [
    # General Financial News
    'https://feeds.reuters.com/reuters/businessNews',
    'https://feeds.reuters.com/Reuters/worldNews',
    'https://www.cnbc.com/id/100003114/device/rss/rss.html',  # Top News
    'https://www.cnbc.com/id/10001147/device/rss/rss.html',  # Economics
    'https://www.cnbc.com/id/15839135/device/rss/rss.html',  # Markets
    'https://www.marketwatch.com/rss/topstories',
    'https://www.marketwatch.com/rss/marketpulse',
    'https://feeds.finance.yahoo.com/rss/2.0/headline',

    # Government/Policy
    'https://www.federalreserve.gov/feeds/press_all.xml',
    'https://home.treasury.gov/rss/press-releases',

    # Business/Corporate
    'https://www.wsj.com/xml/rss/3_7031.xml',  # Economy
    'https://www.wsj.com/xml/rss/3_7014.xml',  # Markets

    # International
    'https://www.ft.com/?format=rss',
    'https://feeds.bbci.co.uk/news/business/rss.xml',
]

# Market Data Symbols
MARKET_SYMBOLS = {
    'stocks': ['^GSPC', '^DJI', '^IXIC', '^VIX'],  # S&P 500, Dow, Nasdaq, VIX
    'commodities': ['GC=F', 'CL=F'],  # Gold, Oil
    'forex': ['EURUSD=X', 'DX-Y.NYB'],  # EUR/USD, Dollar Index
    'bonds': ['^TNX', '^TYX'],  # 10Y and 30Y Treasury yields
}

# FRED API endpoints (free, no key required)
FRED_SERIES = {
    'unemployment': 'UNRATE',
    'inflation': 'CPIAUCSL',
    'gdp': 'GDP',
    'fed_funds': 'DFF',
    '10y_treasury': 'DGS10',
    '2y_treasury': 'DGS2',
}

# Database
DATABASE_PATH = 'data/digests.db'
