#!/usr/bin/env python3
"""
Scheduler for automatic digest generation
Runs the digest generator at specified time each day
"""

import schedule
import time
import logging
from datetime import datetime
import pytz

from app.digest_generator import DigestGenerator
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_daily_digest():
    """Generate the daily digest"""
    logger.info("Starting scheduled digest generation")

    try:
        if not config.ANTHROPIC_API_KEY:
            logger.error("ANTHROPIC_API_KEY not set")
            return

        generator = DigestGenerator(
            rss_feeds=config.RSS_FEEDS,
            db_path=config.DATABASE_PATH,
            anthropic_api_key=config.ANTHROPIC_API_KEY,
            alpha_vantage_key=config.ALPHA_VANTAGE_API_KEY,
        )

        result = generator.generate_digest()

        if result['success']:
            logger.info(f"Successfully generated digest for {result['date']}")
        else:
            logger.error(f"Digest generation failed: {result.get('error')}")

    except Exception as e:
        logger.error(f"Error in scheduled digest generation: {str(e)}", exc_info=True)


def run_scheduler():
    """Run the scheduler"""
    logger.info(f"Starting scheduler - Daily digest at {config.DIGEST_TIME} {config.TIMEZONE}")

    # Schedule the daily digest
    schedule.every().day.at(config.DIGEST_TIME).do(generate_daily_digest)

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == '__main__':
    # Ensure data directory exists
    import os
    os.makedirs('data', exist_ok=True)

    logger.info("Scheduler started")
    logger.info(f"Digest will be generated daily at {config.DIGEST_TIME} {config.TIMEZONE}")

    # Run the scheduler
    run_scheduler()
