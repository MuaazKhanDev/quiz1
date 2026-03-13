"""
Main entry point for the e-commerce scraper.
"""

import time
from src.scraper.crawler import EcommerceCrawler
from src.scraper.parsers import ProductParser, CategoryParser
from src.scraper.exporters import CSVExporter
from src.scraper.utils import deduplicate_products


def main():
    """Main scraping workflow."""
    print("Starting e-commerce scraper...")

    # Initialize components
    base_url = "https://webscraper.io/test-sites/e-commerce/static"
    crawler = EcommerceCrawler(base_url)
    product_parser = ProductParser(base_url)
    category_parser = CategoryParser(base_url)
    exporter = CSVExporter()

    # Step 1: Crawl and collect all product URLs with metadata
    print("Phase 1: Discovering products...")
    products_metadata = crawler.crawl_all_products()
    print(f"Found {len(products_metadata)} product URLs")

    # Step 2: Parse product detail pages
    print("Phase 2: Parsing product details...")
    products = []

    for i, product_meta in enumerate(products_metadata, 1):
        url = product_meta['url']
        category = product_meta['category']
        subcategory = product_meta['subcategory']
        page_ref = f"page_{i}"

        print(f"Processing product {i}/{len(products_metadata)}: {url}")

        product_data = product_parser.parse_product_page(
            url, category, subcategory, page_ref
        )
        if product_data:
            products.append(product_data)

        # Be respectful to the server
        time.sleep(0.5)

    # Step 3: Deduplicate products
    print(f"Before deduplication: {len(products)} products")
    products = deduplicate_products(products)
    print(f"After deduplication: {len(products)} products")

    # Step 4: Export data
    print("Phase 3: Exporting data...")
    exporter.export_products(products)
    exporter.export_category_summary(products)

    print("Scraping completed successfully!")
    print(f"Generated files: data/products.csv, data/category_summary.csv")


if __name__ == "__main__":
    main()
