from typing import Dict, Optional
from bs4 import BeautifulSoup

from .utils import safe_get_text, safe_get_attr, normalize_price, resolve_url, make_request


class ProductParser:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse_product_page(self, url: str, category: str = "", subcategory: str = "",
                          page_ref: str = "") -> Optional[Dict]:
        response = make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        product_data = {
            'url': url,
            'category': category,
            'subcategory': subcategory,
            'page_reference': page_ref
        }

        title_elem = soup.select_one('h4')
        if not title_elem:
            title_elem = soup.select_one('.title, .product-title')
        product_data['title'] = safe_get_text(title_elem)

        price_elem = soup.select_one('[itemprop="price"]')
        price_text = safe_get_text(price_elem)
        product_data['price'] = normalize_price(price_text)

        desc_elem = None
        paragraphs = soup.select('p')
        for p in paragraphs:
            text = safe_get_text(p)
            if ('"' in text or 'GB' in text or 'Windows' in text) and len(text) > 20:
                desc_elem = p
                break
        product_data['description'] = safe_get_text(desc_elem)

        img_elem = soup.select_one('img[src*="/images/test-sites/"]')
        if not img_elem:
            img_elem = soup.select_one('img:not([src*="logo"])')
        img_src = safe_get_attr(img_elem, 'src')
        product_data['image_url'] = resolve_url(self.base_url, img_src) if img_src else ""

        review_elem = soup.select_one('.ratings, .reviews')
        if review_elem:
            review_text = safe_get_text(review_elem)
            product_data['reviews'] = review_text
        else:
            review_candidates = soup.select('*')
            for candidate in review_candidates:
                text = safe_get_text(candidate)
                if 'review' in text.lower():
                    product_data['reviews'] = text
                    break

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

        product_cards = soup.select('.product, .card, .item, [class*="product"]')

        for card in product_cards:
            product = {}

            title_elem = card.select_one('h3, .title, a')
            product['title'] = safe_get_text(title_elem)

            price_elem = card.select_one('.price, [class*="price"]')
            price_text = safe_get_text(price_elem)
            product['price'] = normalize_price(price_text)

            link_elem = card.select_one('a[href*="/product/"]')
            if link_elem:
                href = safe_get_attr(link_elem, 'href')
                product['url'] = resolve_url(self.base_url, href)

            img_elem = card.select_one('img')
            img_src = safe_get_attr(img_elem, 'src')
            product['image_url'] = resolve_url(self.base_url, img_src) if img_src else ""

            desc_elem = card.select_one('.description, p')
            product['description'] = safe_get_text(desc_elem)

            if product.get('title') or product.get('url'):
                products.append(product)

        return products