import anthropic
from typing import List, Dict
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Uses Claude to analyze, rank, and tag news stories"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze_and_rank_stories(
        self, articles: List[Dict], market_data: Dict, top_n: int = 10
    ) -> List[Dict]:
        """
        Analyze articles and return top N ranked by economic impact

        Args:
            articles: List of article dictionaries
            market_data: Current market data
            top_n: Number of top articles to return

        Returns:
            List of analyzed and ranked articles
        """
        if not articles:
            logger.warning("No articles to analyze")
            return []

        # Prepare article summaries for Claude
        article_summaries = []
        for idx, article in enumerate(articles):
            article_summaries.append(
                f"{idx}. {article['title']}\n"
                f"   Source: {article['source']}\n"
                f"   Summary: {article['summary'][:200]}..."
            )

        articles_text = "\n\n".join(article_summaries)

        # Prepare market context
        market_context = self._format_market_data(market_data)

        prompt = f"""You are an expert economic analyst preparing a daily digest for a YouTube series about economic news.

Current Market Context:
{market_context}

Today's News Articles:
{articles_text}

Your task is to:
1. Rank the top {top_n} stories by their LONG-TERM impact on US economic growth and markets
2. For each story, identify:
   - Category: "cold_open" (absurd/destabilizing hook), "macro_shift" (major geopolitical/policy), or "signal_check" (smaller but notable)
   - Key data points (numbers, percentages, dates, companies, people)
   - Market impact analysis: How this affects stocks, sectors, commodities, rates, dollar
   - Importance score (1-10)
   - Why this matters for the economy

Consider:
- Fed policy and interest rates
- Labor market developments
- Geopolitical events affecting trade, energy, or stability
- Major corporate moves that indicate broader trends
- Inflation and growth indicators
- Banking and financial system stability

Return your analysis as a JSON array with this structure:
[
  {{
    "article_index": 0,
    "category": "macro_shift",
    "importance_score": 9,
    "key_data_points": ["unemployment rose to 4.2%", "150k jobs added", "wages up 3.8%"],
    "market_impact": {{
      "stocks": "Negative pressure on growth stocks due to higher rates expectations",
      "bonds": "10Y yield likely to rise as Fed may delay cuts",
      "dollar": "Strengthens on hawkish Fed outlook",
      "commodities": "Gold may fall as real rates rise",
      "sectors": "Financials benefit, tech under pressure"
    }},
    "why_it_matters": "Labor market resilience means Fed stays restrictive longer, affecting all asset prices",
    "hook_potential": "The economy added jobs but somehow that's bad news for stocks"
  }}
]

Return ONLY valid JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse Claude's response
            response_text = response.content[0].text.strip()

            # Extract JSON from response (in case Claude added any extra text)
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1

            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in Claude's response")
                return []

            analysis = json.loads(response_text[json_start:json_end])

            # Merge analysis with original articles
            ranked_articles = []
            for item in analysis[:top_n]:
                idx = item['article_index']
                if 0 <= idx < len(articles):
                    article = articles[idx].copy()
                    article.update({
                        'category': item['category'],
                        'importance_score': item['importance_score'],
                        'key_data_points': item['key_data_points'],
                        'market_impact': item['market_impact'],
                        'why_it_matters': item['why_it_matters'],
                        'hook_potential': item.get('hook_potential', ''),
                    })
                    ranked_articles.append(article)

            logger.info(f"Successfully analyzed and ranked {len(ranked_articles)} articles")
            return ranked_articles

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Claude's JSON response: {str(e)}")
            logger.error(f"Response was: {response_text}")
            return []
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return []

    def _format_market_data(self, market_data: Dict) -> str:
        """Format market data for Claude's context"""
        lines = []

        if market_data.get('stocks'):
            lines.append("Stock Market:")
            for name, data in market_data['stocks'].items():
                lines.append(f"  - {name}: {data['value']} ({data['change']:+.2f}%)")

        if market_data.get('gold'):
            gold = market_data['gold']
            lines.append(f"\nGold: ${gold['value']}/oz ({gold['change']:+.2f}%)")

        if market_data.get('treasuries'):
            lines.append("\nTreasury Yields:")
            for name, data in market_data['treasuries'].items():
                lines.append(f"  - {name}: {data['value']}% ({data['change']:+.3f})")

        if market_data.get('forex'):
            lines.append("\nForex:")
            for name, data in market_data['forex'].items():
                lines.append(f"  - {name}: {data['value']} ({data['change']:+.2f}%)")

        if market_data.get('macro'):
            lines.append("\nMacro Indicators:")
            for name, data in market_data['macro'].items():
                date_str = f" (as of {data['date']})" if 'date' in data else ""
                lines.append(f"  - {name}: {data['value']}{date_str}")

        return "\n".join(lines) if lines else "No market data available"

    def generate_digest_summary(self, ranked_articles: List[Dict]) -> str:
        """Generate a brief summary of the day's key themes"""
        if not ranked_articles:
            return "No significant economic news today."

        article_list = []
        for article in ranked_articles[:5]:
            article_list.append(f"- {article['title']} ({article['category']})")

        articles_text = "\n".join(article_list)

        prompt = f"""Based on today's top economic news, write a 2-3 sentence summary of the key themes and market narrative:

{articles_text}

Focus on: What's the story markets are reacting to today? What's the through-line connecting these stories?"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Market summary unavailable."
