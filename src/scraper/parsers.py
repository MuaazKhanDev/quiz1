"""
Parsers for extracting data from e-commerce pages.
"""

from typing import Dict, Optional
from bs4 import BeautifulSoup

from .utils import safe_get_text, safe_get_attr, normalize_price, resolve_url, make_request


class ProductParser:
    """Parser for product detail pages."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse_product_page(self, url: str, category: str = "", subcategory: str = "",
                          page_ref: str = "") -> Optional[Dict]:
        """Parse a product detail page and extract data."""
        response = make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product information
        product_data = {
            'url': url,
            'category': category,
            'subcategory': subcategory,
            'page_reference': page_ref
        }

        # Product title - look for h1 or title in breadcrumb/structure
        title_elem = soup.select_one('h1')
        if not title_elem:
            # Try to get from URL or other elements
            title_elem = soup.select_one('.breadcrumb a:last-child, .title')
        product_data['title'] = safe_get_text(title_elem)

        # Price - look for price with itemprop or specific classes
        price_elem = soup.select_one('[itemprop="price"]')
        if not price_elem:
            price_elem = soup.select_one('.price, [class*="price"]')
        price_text = safe_get_text(price_elem)
        product_data['price'] = normalize_price(price_text)

        # Description - look for description text
        desc_elem = soup.select_one('.description, p:not(.price)')
        if not desc_elem:
            # Look for any paragraph that might contain description
            paragraphs = soup.select('p')
            for p in paragraphs:
                text = safe_get_text(p)
                if len(text) > 20 and not '$' in text:  # Avoid price paragraphs
                    desc_elem = p
                    break
        product_data['description'] = safe_get_text(desc_elem)

        # Image URL - look for product images, not logos
        img_elem = soup.select_one('img:not([src*="logo"])')
        if not img_elem:
            img_elem = soup.select_one('img')
        img_src = safe_get_attr(img_elem, 'src')
        product_data['image_url'] = resolve_url(self.base_url, img_src) if img_src else ""

        # Review count/rating - look for review information
        review_elem = soup.select_one('.reviews, .rating, [class*="review"], [class*="rating"]')
        product_data['reviews'] = safe_get_text(review_elem)

        # Additional specs/details - look for specifications
        specs_elem = soup.select_one('.specs, .details, .specifications, .spec')
        if not specs_elem:
            # Look for any element that might contain specs
            specs_candidates = soup.select('.row, .col, div')
            for candidate in specs_candidates:
                text = safe_get_text(candidate)
                if len(text) > 10 and not text.startswith('$'):
                    specs_elem = candidate
                    break
        product_data['specifications'] = safe_get_text(specs_elem)

        return product_data


class CategoryParser:
    """Parser for category and listing pages."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse_listing_page(self, url: str) -> list:
        """Parse a product listing page to extract basic product info."""
        response = make_request(url)
        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        # Find product cards/containers
        product_cards = soup.select('.product, .card, .item, [class*="product"]')

        for card in product_cards:
            product = {}

            # Title
            title_elem = card.select_one('h3, .title, a')
            product['title'] = safe_get_text(title_elem)

            # Price
            price_elem = card.select_one('.price, [class*="price"]')
            price_text = safe_get_text(price_elem)
            product['price'] = normalize_price(price_text)

            # Product link
            link_elem = card.select_one('a[href*="/product/"]')
            if link_elem:
                href = safe_get_attr(link_elem, 'href')
                product['url'] = resolve_url(self.base_url, href)

            # Image
            img_elem = card.select_one('img')
            img_src = safe_get_attr(img_elem, 'src')
            product['image_url'] = resolve_url(self.base_url, img_src) if img_src else ""

            # Description (if available on listing page)
            desc_elem = card.select_one('.description, p')
            product['description'] = safe_get_text(desc_elem)

            if product.get('title') or product.get('url'):
                products.append(product)

        return products