import requests
from bs4 import BeautifulSoup

# Test the laptops subcategory page
url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
print(f"\n\nFetching laptops subcategory: {url}...")
response = requests.get(url)
print(f"Response status: {response.status_code}")

soup = BeautifulSoup(response.content, 'html.parser')
print(f"Page title: {soup.title.get_text() if soup.title else 'No title'}")

print('\nAll links on laptops page:')
all_links = soup.select('a')
product_links = []

for link in all_links:
    href = link.get('href')
    text = link.get_text().strip()
    if href and '/product/' in href:
        product_links.append((text, href))

print(f"Product links: {len(product_links)}")
for text, href in product_links[:3]:
    print(f"  {text}: {href}")

# Check for pagination
pagination = soup.select('.pagination, .pager')
print(f"\nPagination elements: {len(pagination)}")
if pagination:
    page_links = pagination[0].select('a')
    print(f"Page links in pagination: {len(page_links)}")
    for link in page_links:
        href = link.get('href')
        text = link.get_text().strip()
        print(f"  {text}: {href}")

# Check total products
product_cards = soup.select('.card, .product, .item')
print(f"\nProduct cards found: {len(product_cards)}")

# Test a product detail page
if product_links:
    product_url = 'https://webscraper.io' + product_links[0][1]
    print(f"\n\nTesting product detail page: {product_url}")
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.select_one('h1, .product-title')
    price = soup.select_one('.price, [class*="price"]')
    desc = soup.select_one('.description, .product-description')
    img = soup.select_one('img')

    print("Product detail extraction:")
    print(f"  Title: {title.get_text().strip() if title else 'Not found'}")
    print(f"  Price: {price.get_text().strip() if price else 'Not found'}")
    print(f"  Description: {desc.get_text().strip() if desc else 'Not found'}")
    print(f"  Image: {img.get('src') if img else 'Not found'}")