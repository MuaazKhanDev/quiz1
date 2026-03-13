import pytest

from scraper.utils import normalize_price, resolve_url, deduplicate_products


def test_normalize_price_usd():
    assert normalize_price('$1,234.56') == 1234.56


def test_normalize_price_euro():
    assert normalize_price('1.234,56') == 1234.56


def test_resolve_url_absolute():
    assert resolve_url('https://example.com', 'https://other.com') == 'https://other.com'


def test_resolve_url_relative():
    assert resolve_url('https://example.com/base', '/path') == 'https://example.com/path'


def test_deduplicate_products():
    products = [
        {'url': 'https://example.com/p1', 'title': 'A'},
        {'url': 'https://example.com/p2', 'title': 'B'},
        {'url': 'https://example.com/p1', 'title': 'A duplicate'},
    ]
    deduped = deduplicate_products(products)
    assert len(deduped) == 2
    assert deduped[0]['url'] == 'https://example.com/p1'
    assert deduped[1]['url'] == 'https://example.com/p2'
