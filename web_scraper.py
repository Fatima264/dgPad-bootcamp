import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Article:
    """Represents an article with its metadata and content."""
    url: str  # URL of the article
    post_id: int  # Unique ID of the article
    title: str  # Title of the article
    keywords: list[str]  # List of keywords associated with the article
    thumbnail: str  # URL of the article's thumbnail image
    publication_date: datetime  # Date and time the article was published
    last_updated_date: datetime  # Date and time the article was last updated
    author: str  # Author of the article
    full_text: str  # Full text content of the article
    summary: str = ""  # Optional summary of the article
    categories: list[str] = None # Optional list of categories the article belongs to
    tags: list[str] = None  # Optional list of tags associated with the article



    class SitemapParser:
        def __init__(self, sitemap_index_url: str):
            self.sitemap_index_url = sitemap_index_url

        def get_sitemap_urls(self) -> List[str]:
            """Retrieve monthly sitemap URLs from the main sitemap index."""
            response = requests.get(self.sitemap_index_url)
            response.raise_for_status()  # Ensure we notice bad responses
            sitemaps = self._parse_sitemap_index(response.content)
            return sitemaps

        def _parse_sitemap_index(self, xml_content: bytes) -> List[str]:
            """Parse the sitemap index XML to extract sitemap URLs."""
            sitemap_urls = []
            root = ET.fromstring(xml_content)
            for sitemap in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
                loc = sitemap.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
                sitemap_urls.append(loc)
            return sitemap_urls

        def get_article_urls(self, sitemap_url: str) -> List[str]:
            """Extract article URLs from a monthly sitemap."""
            response = requests.get(sitemap_url)
            response.raise_for_status()
            article_urls = self._parse_sitemap(response.content)
            return article_urls

        def _parse_sitemap(self, xml_content: bytes) -> List[str]:
            """Parse a sitemap XML to extract article URLs."""
            article_urls = []
            root = ET.fromstring(xml_content)
            for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
                loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
                article_urls.append(loc)
            return article_urls

    # Example usage
    if __name__ == "__main__":
        sitemap_index_url = "https://www.almayadeen.net/sitemaps/all.xml"
        parser = SitemapParser(sitemap_index_url)

        # Get monthly sitemap URLs
        monthly_sitemaps = parser.get_sitemap_urls()
        print("Monthly sitemaps:")
        for sitemap in monthly_sitemaps:
            print(sitemap)

        # Get article URLs from the first monthly sitemap
        if monthly_sitemaps:
            first_sitemap_url = monthly_sitemaps[0]
            article_urls = parser.get_article_urls(first_sitemap_url)
            print("\nArticle URLs from the first monthly sitemap:")
            for url in article_urls:
                print(url)


