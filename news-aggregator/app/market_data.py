import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """Fetches market data from various sources"""

    def __init__(self, alpha_vantage_key: Optional[str] = None):
        self.alpha_vantage_key = alpha_vantage_key

    def fetch_all_data(self) -> Dict:
        """
        Fetch all market data

        Returns:
            Dictionary containing all market data
        """
        data = {
            'stocks': self._fetch_stock_data(),
            'gold': self._fetch_gold_data(),
            'treasuries': self._fetch_treasury_data(),
            'forex': self._fetch_forex_data(),
            'macro': self._fetch_macro_data(),
            'timestamp': datetime.now().isoformat(),
        }

        return data

    def _fetch_stock_data(self) -> Dict:
        """Fetch major stock indices"""
        symbols = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^VIX': 'VIX',
        }

        stock_data = {}

        for symbol, name in symbols.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d')

                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100

                    stock_data[name] = {
                        'value': round(current, 2),
                        'change': round(change, 2),
                        'symbol': symbol,
                    }

            except Exception as e:
                logger.error(f"Error fetching {symbol}: {str(e)}")
                continue

        return stock_data

    def _fetch_gold_data(self) -> Dict:
        """Fetch gold price"""
        try:
            ticker = yf.Ticker('GC=F')
            hist = ticker.history(period='5d')

            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change = ((current - previous) / previous) * 100

                return {
                    'value': round(current, 2),
                    'change': round(change, 2),
                    'unit': 'USD/oz',
                }
        except Exception as e:
            logger.error(f"Error fetching gold data: {str(e)}")

        return {}

    def _fetch_treasury_data(self) -> Dict:
        """Fetch treasury yields from FRED"""
        treasury_data = {}

        # Using Yahoo Finance for treasury yields
        treasury_symbols = {
            '^TNX': '10-Year Treasury',
            '^FVX': '5-Year Treasury',
            '^TYX': '30-Year Treasury',
        }

        for symbol, name in treasury_symbols.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d')

                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = current - previous

                    treasury_data[name] = {
                        'value': round(current, 3),
                        'change': round(change, 3),
                        'unit': '%',
                    }

            except Exception as e:
                logger.error(f"Error fetching {symbol}: {str(e)}")
                continue

        return treasury_data

    def _fetch_forex_data(self) -> Dict:
        """Fetch forex data"""
        forex_data = {}

        try:
            # Dollar Index
            ticker = yf.Ticker('DX-Y.NYB')
            hist = ticker.history(period='5d')

            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change = ((current - previous) / previous) * 100

                forex_data['Dollar Index'] = {
                    'value': round(current, 2),
                    'change': round(change, 2),
                }
        except Exception as e:
            logger.error(f"Error fetching forex data: {str(e)}")

        return forex_data

    def _fetch_macro_data(self) -> Dict:
        """Fetch macro economic data from FRED"""
        macro_data = {}

        # Note: FRED data is typically not updated daily
        # We'll fetch the most recent values

        fred_series = {
            'DFF': 'Fed Funds Rate',
            'UNRATE': 'Unemployment Rate',
        }

        for series_id, name in fred_series.items():
            try:
                # FRED JSON API (no key required for basic access)
                url = f'https://api.stlouisfed.org/fred/series/observations'
                params = {
                    'series_id': series_id,
                    'api_key': 'demo',  # Using demo key for basic access
                    'file_type': 'json',
                    'sort_order': 'desc',
                    'limit': 2,
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if 'observations' in data and len(data['observations']) > 0:
                        latest = data['observations'][0]
                        if latest['value'] != '.':
                            macro_data[name] = {
                                'value': float(latest['value']),
                                'date': latest['date'],
                            }

            except Exception as e:
                logger.error(f"Error fetching FRED data for {series_id}: {str(e)}")
                continue

        return macro_data

    def get_market_summary(self) -> str:
        """Generate a text summary of current market conditions"""
        data = self.fetch_all_data()

        summary_parts = []

        # Stock market
        if data['stocks']:
            sp500 = data['stocks'].get('S&P 500', {})
            if sp500:
                summary_parts.append(
                    f"S&P 500: {sp500['value']} ({sp500['change']:+.2f}%)"
                )

        # Gold
        if data['gold']:
            summary_parts.append(
                f"Gold: ${data['gold']['value']}/oz ({data['gold']['change']:+.2f}%)"
            )

        # 10Y Treasury
        if data['treasuries']:
            ten_year = data['treasuries'].get('10-Year Treasury', {})
            if ten_year:
                summary_parts.append(
                    f"10Y Treasury: {ten_year['value']}%"
                )

        return " | ".join(summary_parts) if summary_parts else "Market data unavailable"
