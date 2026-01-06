from datetime import datetime
from typing import Dict
import logging

from app.news_aggregator import NewsAggregator
from app.market_data import MarketDataFetcher
from app.ai_analyzer import AIAnalyzer
from app.database import DigestDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DigestGenerator:
    """Orchestrates the daily digest generation"""

    def __init__(
        self,
        rss_feeds: list,
        db_path: str,
        anthropic_api_key: str,
        alpha_vantage_key: str = None,
    ):
        self.news_aggregator = NewsAggregator(rss_feeds)
        self.market_fetcher = MarketDataFetcher(alpha_vantage_key)
        self.ai_analyzer = AIAnalyzer(anthropic_api_key)
        self.db = DigestDatabase(db_path)

    def generate_digest(self, hours_back: int = 24) -> Dict:
        """
        Generate a complete daily digest

        Args:
            hours_back: Number of hours to look back for news

        Returns:
            Dictionary containing the complete digest
        """
        logger.info("Starting digest generation")

        # 1. Fetch news articles
        logger.info("Fetching news articles...")
        articles = self.news_aggregator.fetch_articles(hours_back=hours_back)

        if not articles:
            logger.warning("No articles found")
            return {
                'success': False,
                'error': 'No articles found',
                'date': datetime.now().strftime('%Y-%m-%d'),
            }

        # 2. Fetch market data
        logger.info("Fetching market data...")
        market_data = self.market_fetcher.fetch_all_data()

        # 3. Analyze and rank articles
        logger.info("Analyzing articles with AI...")
        ranked_articles = self.ai_analyzer.analyze_and_rank_stories(
            articles, market_data, top_n=10
        )

        if not ranked_articles:
            logger.warning("AI analysis returned no results")
            return {
                'success': False,
                'error': 'AI analysis failed',
                'date': datetime.now().strftime('%Y-%m-%d'),
            }

        # 4. Generate summary
        logger.info("Generating digest summary...")
        summary = self.ai_analyzer.generate_digest_summary(ranked_articles)

        # 5. Save to database
        date_str = datetime.now().strftime('%Y-%m-%d')
        digest_id = self.db.save_digest(
            date=date_str,
            articles=ranked_articles,
            market_data=market_data,
            summary=summary,
        )

        logger.info(f"Digest generation complete! Digest ID: {digest_id}")

        return {
            'success': True,
            'date': date_str,
            'digest_id': digest_id,
            'articles': ranked_articles,
            'market_data': market_data,
            'summary': summary,
        }
