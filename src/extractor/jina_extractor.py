"""
Simple and free content extractor using Jina AI Reader.
No API key required for basic usage.
"""
import requests
from typing import List, Dict, Optional
import time


class JinaExtractor:
    """
    Extracts text content using Jina AI Reader API.

    Free tier: 20 requests/min without key, 200/min with free key.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Jina extractor.

        Args:
            api_key: Optional Jina API key for higher rate limits
        """
        self.api_key = api_key
        self.base_url = "https://r.jina.ai/"
        self.search_url = "https://s.jina.ai/"

    def extract_url(self, url: str) -> Dict[str, str]:
        """
        Extract clean text content from a URL.

        Args:
            url: The URL to extract content from

        Returns:
            Dictionary with title, url, and content
        """
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        try:
            response = requests.get(
                f"{self.base_url}{url}",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            content = response.text

            # Extract title from markdown (usually first # heading)
            title = ""
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            return {
                'title': title,
                'url': url,
                'content': content,
                'source_type': 'web'
            }

        except Exception as e:
            raise Exception(f"Failed to extract content from {url}: {str(e)}")

    def extract_multiple(self, urls: List[str], delay: float = 3.0) -> List[Dict]:
        """
        Extract content from multiple URLs.

        Args:
            urls: List of URLs to extract
            delay: Delay between requests (default 3s for free tier)

        Returns:
            List of extracted content dictionaries
        """
        results = []

        for i, url in enumerate(urls):
            try:
                print(f"Extracting {i+1}/{len(urls)}: {url}")
                result = self.extract_url(url)
                results.append(result)

                # Rate limiting
                if i < len(urls) - 1:
                    time.sleep(delay)

            except Exception as e:
                print(f"Error extracting {url}: {e}")
                continue

        return results

    def search_and_extract(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search the web and extract content from top results.

        Args:
            query: Search query
            num_results: Number of results to extract (default 5)

        Returns:
            List of extracted content dictionaries
        """
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        try:
            # Jina search returns top 5 results with content
            response = requests.get(
                f"{self.search_url}?q={query}",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            # Parse the search results (they come as markdown)
            content = response.text

            # For now, return the raw search results
            # In production, you'd parse individual results
            return [{
                'title': f"Search results for: {query}",
                'url': f"{self.search_url}?q={query}",
                'content': content,
                'source_type': 'search'
            }]

        except Exception as e:
            raise Exception(f"Failed to search for '{query}': {str(e)}")

    def extract_powell_speeches(self, num_speeches: int = 10) -> List[Dict]:
        """
        Extract Jerome Powell speeches from Federal Reserve website.

        Args:
            num_speeches: Number of recent speeches to extract

        Returns:
            List of extracted speeches
        """
        # Curated list of recent Powell speeches
        powell_urls = [
            "https://www.federalreserve.gov/newsevents/speech/powell20241218a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20241204a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20241114a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20241107a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240930a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240826a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240731a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240612a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240501a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240320a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20240131a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20231213a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20231201a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20231109a.htm",
            "https://www.federalreserve.gov/newsevents/speech/powell20231019a.htm",
        ]

        # Limit to requested number
        urls_to_extract = powell_urls[:num_speeches]

        print(f"Extracting {len(urls_to_extract)} Powell speeches...")
        return self.extract_multiple(urls_to_extract)
