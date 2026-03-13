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

        # Product title - look for h4 (product name) not h1 (site name)
        title_elem = soup.select_one('h4')
        if not title_elem:
            title_elem = soup.select_one('.title, .product-title')
        product_data['title'] = safe_get_text(title_elem)

        # Price - look for price with itemprop
        price_elem = soup.select_one('[itemprop="price"]')
        price_text = safe_get_text(price_elem)
        product_data['price'] = normalize_price(price_text)

        # Description - look for the paragraph with product specs
        desc_elem = None
        paragraphs = soup.select('p')
        for p in paragraphs:
            text = safe_get_text(p)
            # Look for paragraph with product specs (contains inches, GB, etc.)
            if ('"' in text or 'GB' in text or 'Windows' in text) and len(text) > 20:
                desc_elem = p
                break
        product_data['description'] = safe_get_text(desc_elem)

        # Image URL - look for product images, not logos
        img_elem = soup.select_one('img[src*="/images/test-sites/"]')
        if not img_elem:
            img_elem = soup.select_one('img:not([src*="logo"])')
        img_src = safe_get_attr(img_elem, 'src')
        product_data['image_url'] = resolve_url(self.base_url, img_src) if img_src else ""

        # Review count/rating - look for review information
        review_elem = soup.select_one('.ratings, .reviews')
        if review_elem:
            review_text = safe_get_text(review_elem)
            product_data['reviews'] = review_text
        else:
            # Look for review count in the page
            review_candidates = soup.select('*')
            for candidate in review_candidates:
                text = safe_get_text(candidate)
                if 'review' in text.lower():
                    product_data['reviews'] = text
                    break

        # Additional specs/details - use the description as specs
        product_data['specifications'] = product_data['description']

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