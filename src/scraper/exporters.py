import csv
from typing import List, Dict
from collections import defaultdict
import os


class CSVExporter:
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_products(self, products: List[Dict], filename: str = "products.csv"):
        filepath = os.path.join(self.output_dir, filename)

        if not products:
            print("No products to export")
            return

        headers = [
            'category', 'subcategory', 'title', 'price', 'url', 'image_url',
            'description', 'reviews', 'specifications', 'page_reference'
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for product in products:
                row = {header: product.get(header, '') for header in headers}
                writer.writerow(row)

        print(f"Exported {len(products)} products to {filepath}")

    def export_category_summary(self, products: List[Dict], filename: str = "category_summary.csv"):
        filepath = os.path.join(self.output_dir, filename)

        if not products:
            print("No products for summary")
            return

        subcategory_stats = defaultdict(lambda: {
            'total_products': 0,
            'prices': [],
            'missing_descriptions': 0,
            'duplicates_removed': 0
        })

        seen_urls = set()

        for product in products:
            subcategory = product.get('subcategory', 'Unknown')
            price = product.get('price', 0)
            description = product.get('description', '').strip()
            url = product.get('url', '')

            stats = subcategory_stats[subcategory]
            stats['total_products'] += 1

            if price > 0:
                stats['prices'].append(price)

            if not description:
                stats['missing_descriptions'] += 1

            if url in seen_urls:
                stats['duplicates_removed'] += 1
            else:
                seen_urls.add(url)

        summary_data = []
        for subcategory, stats in subcategory_stats.items():
            prices = stats['prices']
            summary_data.append({
                'subcategory': subcategory,
                'total_products': stats['total_products'],
                'average_price': round(sum(prices) / len(prices), 2) if prices else 0,
                'min_price': min(prices) if prices else 0,
                'max_price': max(prices) if prices else 0,
                'missing_descriptions': stats['missing_descriptions'],
                'duplicates_removed': stats['duplicates_removed']
            })

        summary_data.sort(key=lambda x: x['subcategory'])

        headers = [
            'subcategory', 'total_products', 'average_price', 'min_price', 'max_price',
            'missing_descriptions', 'duplicates_removed'
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(summary_data)

        print(f"Exported category summary to {filepath}")