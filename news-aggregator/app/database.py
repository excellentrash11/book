import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DigestDatabase:
    """Handles storage and retrieval of daily digests"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS digests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL UNIQUE,
                    summary TEXT,
                    market_data TEXT,
                    created_at TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    digest_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    source TEXT,
                    summary TEXT,
                    category TEXT,
                    importance_score INTEGER,
                    key_data_points TEXT,
                    market_impact TEXT,
                    why_it_matters TEXT,
                    hook_potential TEXT,
                    published TEXT,
                    FOREIGN KEY (digest_id) REFERENCES digests (id)
                )
            ''')

            conn.commit()
            logger.info("Database initialized")

    def save_digest(
        self,
        date: str,
        articles: List[Dict],
        market_data: Dict,
        summary: str = ""
    ) -> int:
        """
        Save a daily digest

        Args:
            date: Date string (YYYY-MM-DD)
            articles: List of analyzed articles
            market_data: Market data dictionary
            summary: Brief summary of the day's themes

        Returns:
            Digest ID
        """
        with sqlite3.connect(self.db_path) as conn:
            # Insert digest
            cursor = conn.execute(
                '''
                INSERT OR REPLACE INTO digests (date, summary, market_data, created_at)
                VALUES (?, ?, ?, ?)
                ''',
                (date, summary, json.dumps(market_data), datetime.now().isoformat())
            )

            digest_id = cursor.lastrowid

            # Delete old articles for this digest (if replacing)
            conn.execute('DELETE FROM articles WHERE digest_id = ?', (digest_id,))

            # Insert articles
            for article in articles:
                conn.execute(
                    '''
                    INSERT INTO articles (
                        digest_id, title, link, source, summary, category,
                        importance_score, key_data_points, market_impact,
                        why_it_matters, hook_potential, published
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        digest_id,
                        article['title'],
                        article['link'],
                        article.get('source', ''),
                        article.get('summary', ''),
                        article.get('category', ''),
                        article.get('importance_score', 0),
                        json.dumps(article.get('key_data_points', [])),
                        json.dumps(article.get('market_impact', {})),
                        article.get('why_it_matters', ''),
                        article.get('hook_potential', ''),
                        article.get('published', datetime.now()).isoformat()
                        if isinstance(article.get('published'), datetime)
                        else str(article.get('published', '')),
                    )
                )

            conn.commit()
            logger.info(f"Saved digest for {date} with {len(articles)} articles")
            return digest_id

    def get_digest(self, date: str) -> Optional[Dict]:
        """
        Get a digest by date

        Args:
            date: Date string (YYYY-MM-DD)

        Returns:
            Digest dictionary or None if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Get digest
            digest_row = conn.execute(
                'SELECT * FROM digests WHERE date = ?', (date,)
            ).fetchone()

            if not digest_row:
                return None

            digest = dict(digest_row)
            digest['market_data'] = json.loads(digest['market_data'])

            # Get articles
            article_rows = conn.execute(
                '''
                SELECT * FROM articles
                WHERE digest_id = ?
                ORDER BY importance_score DESC
                ''',
                (digest['id'],)
            ).fetchall()

            articles = []
            for row in article_rows:
                article = dict(row)
                article['key_data_points'] = json.loads(article['key_data_points'])
                article['market_impact'] = json.loads(article['market_impact'])
                articles.append(article)

            digest['articles'] = articles
            return digest

    def get_latest_digest(self) -> Optional[Dict]:
        """Get the most recent digest"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            digest_row = conn.execute(
                'SELECT * FROM digests ORDER BY date DESC LIMIT 1'
            ).fetchone()

            if not digest_row:
                return None

            date = digest_row['date']
            return self.get_digest(date)

    def list_digests(self, limit: int = 30) -> List[Dict]:
        """
        List recent digests

        Args:
            limit: Maximum number of digests to return

        Returns:
            List of digest summaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                '''
                SELECT date, summary, created_at,
                       (SELECT COUNT(*) FROM articles WHERE digest_id = digests.id) as article_count
                FROM digests
                ORDER BY date DESC
                LIMIT ?
                ''',
                (limit,)
            ).fetchall()

            return [dict(row) for row in rows]
