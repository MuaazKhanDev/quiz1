import re
from urllib.parse import urljoin, urlparse


def clean_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split()).strip()


def normalize_price(price_text: str) -> float:
    if not price_text:
        return 0.0

    cleaned = re.sub(r'[^\d.,]', '', price_text.strip())

    if ',' in cleaned and '.' in cleaned:
        last_comma = cleaned.rfind(',')
        last_dot = cleaned.rfind('.')
        if last_dot > last_comma:
            cleaned = cleaned.replace(',', '')
        else:
            cleaned = cleaned.replace('.', '')
            cleaned = cleaned.replace(',', '.')
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.')

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def resolve_url(base_url: str, relative_url: str) -> str:
    if not relative_url:
        return ""

    if urlparse(relative_url).scheme:
        return relative_url

    return urljoin(base_url, relative_url)


def safe_get_text(element, default: str = "") -> str:
    if element:
        return clean_text(element.get_text())
    return default


def safe_get_attr(element, attr: str, default: str = "") -> str:
    if element and element.has_attr(attr):
        return element[attr]
    return default


def deduplicate_products(products: list) -> list:
    seen_urls = set()
    unique_products = []

    for product in products:
        url = product.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_products.append(product)

    return unique_products


def make_request(url: str, session=None, timeout: int = 10):
    try:
        if session:
            response = session.get(url, timeout=timeout)
        else:
            import requests
            response = requests.get(url, timeout=timeout)

        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Error requesting {url}: {e}")
        return None