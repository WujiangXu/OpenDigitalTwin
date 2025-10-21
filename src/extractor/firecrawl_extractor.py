"""
Best performance content extractor using Firecrawl + Tavily.
Requires API keys but offers superior quality and features.
"""
from typing import List, Dict, Optional
import os

try:
    from firecrawl import FirecrawlApp
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False


class FirecrawlExtractor:
    """
    High-performance extractor using Firecrawl for scraping and Tavily for search.

    Features:
    - Handles JavaScript-heavy pages (96% web coverage)
    - Clean Markdown/JSON output
    - Intelligent search with Tavily
    - PDF and image support
    """

    def __init__(self, firecrawl_api_key: Optional[str] = None,
                 tavily_api_key: Optional[str] = None):
        """
        Initialize Firecrawl extractor.

        Args:
            firecrawl_api_key: Firecrawl API key
            tavily_api_key: Tavily API key for search
        """
        if not FIRECRAWL_AVAILABLE:
            raise ImportError(
                "Firecrawl not installed. Install with: pip install firecrawl-py"
            )

        self.firecrawl_key = firecrawl_api_key or os.getenv('FIRECRAWL_API_KEY')
        self.tavily_key = tavily_api_key or os.getenv('TAVILY_API_KEY')

        if not self.firecrawl_key:
            raise ValueError("FIRECRAWL_API_KEY is required")

        self.firecrawl = FirecrawlApp(api_key=self.firecrawl_key)

        if self.tavily_key and TAVILY_AVAILABLE:
            self.tavily = TavilyClient(api_key=self.tavily_key)
        else:
            self.tavily = None

    def extract_url(self, url: str, formats: List[str] = None) -> Dict[str, str]:
        """
        Extract content from a URL using Firecrawl.

        Args:
            url: The URL to scrape
            formats: Output formats (default: ['markdown'])

        Returns:
            Dictionary with title, url, content, and metadata
        """
        if formats is None:
            formats = ['markdown']

        try:
            # Scrape the URL (updated API)
            result = self.firecrawl.scrape(
                url=url,
                formats=formats
            )

            # Handle both dict and Document object returns
            if hasattr(result, 'markdown'):
                content = result.markdown or getattr(result, 'content', '')
                metadata = getattr(result, 'metadata', {})
                title = metadata.get('title', '') if isinstance(metadata, dict) else getattr(metadata, 'title', '')
            else:
                content = result.get('markdown', '') or result.get('content', '')
                title = result.get('metadata', {}).get('title', '')
                metadata = result.get('metadata', {})

            return {
                'title': title,
                'url': url,
                'content': content,
                'metadata': metadata if isinstance(metadata, dict) else {},
                'source_type': 'web'
            }

        except Exception as e:
            raise Exception(f"Failed to extract content from {url}: {str(e)}")

    def extract_multiple(self, urls: List[str]) -> List[Dict]:
        """
        Extract content from multiple URLs.

        Args:
            urls: List of URLs to extract

        Returns:
            List of extracted content dictionaries
        """
        results = []

        for i, url in enumerate(urls):
            try:
                print(f"Extracting {i+1}/{len(urls)}: {url}")
                result = self.extract_url(url)
                results.append(result)

            except Exception as e:
                print(f"Error extracting {url}: {e}")
                continue

        return results

    def search_tavily(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search using Tavily and return results with content.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results with extracted content
        """
        if not self.tavily:
            raise ValueError("Tavily API key not configured")

        try:
            # Search with Tavily
            search_results = self.tavily.search(
                query=query,
                max_results=num_results,
                include_raw_content=True
            )

            results = []
            for item in search_results.get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('raw_content', '') or item.get('content', ''),
                    'score': item.get('score', 0),
                    'source_type': 'search'
                })

            return results

        except Exception as e:
            raise Exception(f"Failed to search with Tavily: {str(e)}")

    def search_and_extract(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search using Tavily and extract full content using Firecrawl.

        Args:
            query: Search query
            num_results: Number of results to extract

        Returns:
            List of extracted content with full text
        """
        if not self.tavily:
            raise ValueError("Tavily API key required for search")

        try:
            # First search with Tavily
            print(f"Searching for: {query}")
            search_results = self.tavily.search(
                query=query,
                max_results=num_results
            )

            # Extract full content from each result
            results = []
            for i, item in enumerate(search_results.get('results', [])):
                url = item.get('url', '')
                if not url:
                    continue

                try:
                    print(f"Extracting full content {i+1}/{num_results}: {url}")
                    extracted = self.extract_url(url)
                    extracted['search_score'] = item.get('score', 0)
                    results.append(extracted)

                except Exception as e:
                    print(f"Error extracting {url}: {e}")
                    # Fallback to Tavily's content if Firecrawl fails
                    results.append({
                        'title': item.get('title', ''),
                        'url': url,
                        'content': item.get('content', ''),
                        'search_score': item.get('score', 0),
                        'source_type': 'search'
                    })

            return results

        except Exception as e:
            raise Exception(f"Failed to search and extract: {str(e)}")

    def extract_powell_speeches(self, num_speeches: int = 10) -> List[Dict]:
        """
        Extract Jerome Powell speeches using intelligent search + scraping.

        Args:
            num_speeches: Number of speeches to extract

        Returns:
            List of extracted speeches
        """
        if self.tavily:
            # Use Tavily search for best results
            print("Searching for Powell speeches using Tavily...")
            query = "Jerome Powell FOMC speech press conference site:federalreserve.gov"
            return self.search_and_extract(query, num_results=num_speeches)
        else:
            # Fallback to curated URLs
            print("Using curated Powell speech URLs...")
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
            urls_to_extract = powell_urls[:num_speeches]
            return self.extract_multiple(urls_to_extract)
