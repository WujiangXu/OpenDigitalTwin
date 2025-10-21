"""
Factory for creating the appropriate extractor based on configuration.
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv('config/.env')


def create_extractor(extractor_type: Optional[str] = None):
    """
    Create an extractor instance based on configuration.

    Args:
        extractor_type: Type of extractor ('jina' or 'firecrawl').
                       If None, uses EXTRACTOR_TYPE from environment.

    Returns:
        Extractor instance (JinaExtractor or FirecrawlExtractor)
    """
    if extractor_type is None:
        extractor_type = os.getenv('EXTRACTOR_TYPE', 'jina').lower()

    if extractor_type == 'jina':
        from .jina_extractor import JinaExtractor
        jina_key = os.getenv('JINA_API_KEY')
        return JinaExtractor(api_key=jina_key)

    elif extractor_type == 'firecrawl':
        from .firecrawl_extractor import FirecrawlExtractor
        firecrawl_key = os.getenv('FIRECRAWL_API_KEY')
        tavily_key = os.getenv('TAVILY_API_KEY')
        return FirecrawlExtractor(
            firecrawl_api_key=firecrawl_key,
            tavily_api_key=tavily_key
        )

    else:
        raise ValueError(f"Unknown extractor type: {extractor_type}")


def get_extractor_info():
    """
    Get information about available extractors.

    Returns:
        Dictionary with extractor information
    """
    return {
        'jina': {
            'name': 'Jina AI Reader',
            'cost': 'FREE (20 req/min without key, 200 req/min with free key)',
            'features': ['Clean text extraction', 'PDF support', 'Image captions'],
            'api_key_required': False,
            'recommended_for': 'Simple use cases, no API key needed'
        },
        'firecrawl': {
            'name': 'Firecrawl + Tavily',
            'cost': 'FREE tier available (limited usage)',
            'features': [
                'JavaScript rendering',
                '96% web coverage',
                'Intelligent search',
                'High-quality extraction'
            ],
            'api_key_required': True,
            'recommended_for': 'Best performance, complex sites'
        }
    }
