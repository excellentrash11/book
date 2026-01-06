from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import os
import logging

from app.digest_generator import DigestGenerator
from app.database import DigestDatabase
import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize components
db = DigestDatabase(config.DATABASE_PATH)


def get_digest_generator():
    """Create a DigestGenerator instance"""
    if not config.ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set in environment")

    return DigestGenerator(
        rss_feeds=config.RSS_FEEDS,
        db_path=config.DATABASE_PATH,
        anthropic_api_key=config.ANTHROPIC_API_KEY,
        alpha_vantage_key=config.ALPHA_VANTAGE_API_KEY,
    )


@app.route('/')
def index():
    """Home page - shows latest digest"""
    digest = db.get_latest_digest()

    if not digest:
        return render_template('empty.html')

    return render_template('digest.html', digest=digest, is_latest=True)


@app.route('/digest/<date>')
def view_digest(date):
    """View a specific digest by date"""
    digest = db.get_digest(date)

    if not digest:
        return render_template('error.html', error=f"No digest found for {date}"), 404

    return render_template('digest.html', digest=digest, is_latest=False)


@app.route('/history')
def history():
    """View list of all digests"""
    digests = db.list_digests(limit=60)
    return render_template('history.html', digests=digests)


@app.route('/generate', methods=['POST'])
def generate_digest():
    """Manually trigger digest generation"""
    try:
        generator = get_digest_generator()
        result = generator.generate_digest()

        if result['success']:
            return jsonify({
                'success': True,
                'message': f"Digest generated for {result['date']}",
                'date': result['date'],
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
            }), 500

    except Exception as e:
        logger.error(f"Error generating digest: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
        }), 500


@app.route('/api/digest/latest')
def api_latest_digest():
    """API endpoint for latest digest"""
    digest = db.get_latest_digest()

    if not digest:
        return jsonify({'error': 'No digest found'}), 404

    return jsonify(digest)


@app.route('/api/digest/<date>')
def api_get_digest(date):
    """API endpoint for specific digest"""
    digest = db.get_digest(date)

    if not digest:
        return jsonify({'error': f'No digest found for {date}'}), 404

    return jsonify(digest)


@app.template_filter('format_date')
def format_date(date_str):
    """Format date string for display"""
    try:
        date = datetime.fromisoformat(date_str)
        return date.strftime('%B %d, %Y')
    except:
        return date_str


@app.template_filter('format_datetime')
def format_datetime(datetime_str):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(datetime_str)
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return datetime_str


if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
