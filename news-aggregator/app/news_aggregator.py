import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsAggregator:
    """Aggregates news from RSS feeds"""

    def __init__(self, feed_urls: List[str]):
        self.feed_urls = feed_urls

    def fetch_articles(self, hours_back: int = 24) -> List[Dict]:
        """
        Fetch articles from all RSS feeds from the last N hours

        Args:
            hours_back: Number of hours to look back for articles

        Returns:
            List of article dictionaries
        """
        articles = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)

        logger.info(f"Fetching articles from {len(self.feed_urls)} feeds")

        for feed_url in self.feed_urls:
            try:
                feed = feedparser.parse(feed_url)

                for entry in feed.entries:
                    # Parse publication date
                    pub_date = self._parse_date(entry)

                    # Skip old articles
                    if pub_date and pub_date < cutoff_time:
                        continue

                    article = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'summary': entry.get('summary', entry.get('description', '')),
                        'published': pub_date,
                        'source': feed.feed.get('title', feed_url),
                    }

                    # Only add if we have at least a title and link
                    if article['title'] and article['link']:
                        articles.append(article)

            except Exception as e:
                logger.error(f"Error fetching feed {feed_url}: {str(e)}")
                continue

        # Remove duplicates based on title similarity
        articles = self._deduplicate_articles(articles)

        logger.info(f"Fetched {len(articles)} unique articles")
        return articles

    def _parse_date(self, entry) -> datetime:
        """Parse date from feed entry"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                return datetime(*entry.published_parsed[:6])
            except:
                pass

        if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            try:
                return datetime(*entry.updated_parsed[:6])
            except:
                pass

        # Default to now if we can't parse
        return datetime.now()

    def _deduplicate_articles(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []

        for article in articles:
            # Normalize title for comparison
            normalized_title = article['title'].lower().strip()

            # Simple deduplication - could be improved with fuzzy matching
            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_articles.append(article)

        return unique_articles
