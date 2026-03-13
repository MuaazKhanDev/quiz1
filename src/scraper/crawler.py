"""
Crawler module for navigating the e-commerce site.
"""

import time
from typing import List, Dict, Set
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .utils import resolve_url, make_request


class EcommerceCrawler:
    """Crawler for the e-commerce test site."""

    def __init__(self, base_url: str = "https://webscraper.io/test-sites/e-commerce/static"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a page."""
        response = make_request(url, self.session)
        if response:
            return BeautifulSoup(response.content, 'html.parser')
        return None

    def discover_categories(self) -> List[Dict[str, str]]:
        """Discover all categories from the main page."""
        soup = self.get_page(self.base_url)
        if not soup:
            return []

        categories = []
        # Look for category links - they are direct links like /computers, /phones
        category_selectors = [
            'a[href*="/computers"]',
            'a[href*="/phones"]',
            'a[href="/test-sites/e-commerce/static/computers"]',
            'a[href="/test-sites/e-commerce/static/phones"]'
        ]

        seen_urls = set()
        for selector in category_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = resolve_url(self.base_url, href)
                    name = link.get_text().strip()
                    if name and full_url not in seen_urls and full_url != self.base_url:
                        categories.append({
                            'name': name,
                            'url': full_url
                        })
                        seen_urls.add(full_url)

        return categories

    def discover_subcategories(self, category_url: str) -> List[Dict[str, str]]:
        """Discover subcategories within a category."""
        soup = self.get_page(category_url)
        if not soup:
            return []

        subcategories = []
        # Look for subcategory links - they contain paths like /computers/laptops
        subcategory_links = soup.select('a[href*="/computers/"], a[href*="/phones/"]')

        for link in subcategory_links:
            href = link.get('href')
            if href:
                full_url = resolve_url(self.base_url, href)
                name = link.get_text().strip()
                # Only include actual subcategories, not the category itself
                if (name and
                    full_url != category_url and
                    full_url.count('/') > category_url.count('/')):
                    subcategories.append({
                        'name': name,
                        'url': full_url
                    })

        return subcategories

    def get_paginated_pages(self, subcategory_url: str) -> List[str]:
        """Get all paginated pages for a subcategory."""
        pages = [subcategory_url]

        soup = self.get_page(subcategory_url)
        if not soup:
            return pages

        # Look for pagination links
        pagination_links = soup.select('a[href*="page="], .pagination a')

        for link in pagination_links:
            href = link.get('href')
            if href and 'page=' in href:
                full_url = resolve_url(self.base_url, href)
                if full_url not in pages:
                    pages.append(full_url)

        return pages

    def collect_product_links(self, page_url: str) -> List[str]:
        """Collect product links from a listing page."""
        soup = self.get_page(page_url)
        if not soup:
            return []

        product_links = []
        # Look for product links - typically in product cards
        product_elements = soup.select('a[href*="/product/"], .product a, .card a')

        for link in product_elements:
            href = link.get('href')
            if href and '/product/' in href:
                full_url = resolve_url(self.base_url, href)
                if full_url not in product_links:
                    product_links.append(full_url)

        return product_links

    def crawl_all_products(self) -> List[str]:
        """Crawl all categories, subcategories, and collect product URLs."""
        all_product_urls = set()

        categories = self.discover_categories()
        print(f"Found {len(categories)} categories")

        for category in categories:
            print(f"Processing category: {category['name']}")
            subcategories = self.discover_subcategories(category['url'])

            if not subcategories:
                # If no subcategories, treat category as subcategory
                subcategories = [category]

            for subcategory in subcategories:
                print(f"  Processing subcategory: {subcategory['name']}")
                pages = self.get_paginated_pages(subcategory['url'])

                for page_url in pages:
                    print(f"    Processing page: {page_url}")
                    product_urls = self.collect_product_links(page_url)
                    all_product_urls.update(product_urls)

                    # Be respectful to the server
                    time.sleep(0.5)

        return list(all_product_urls)
