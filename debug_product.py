import requests
from bs4 import BeautifulSoup

url = 'https://webscraper.io/test-sites/e-commerce/static/product/38'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print('Page title:', soup.title.get_text() if soup.title else 'No title')
print('H1 tags:', [h.get_text().strip() for h in soup.select('h1')])

# Look for price
price_elements = soup.select('[itemprop="price"]')
print('Price elements:', [p.get_text().strip() for p in price_elements])

print('All paragraphs:')
for i, p in enumerate(soup.select('p')[:5]):
    print(f'  {i}: {p.get_text().strip()[:100]}...')

print('Images:')
for i, img in enumerate(soup.select('img')[:3]):
    print(f'  {i}: {img.get("src")}')

# Look for product name in different places
print('Looking for product name:')
name_candidates = soup.select('h1, .title, .product-title, .name')
for candidate in name_candidates:
    print(f'  {candidate.name}: {candidate.get_text().strip()}')

# Look at the breadcrumb
breadcrumb = soup.select('.breadcrumb, .breadcrumb-item')
print('Breadcrumb:', [b.get_text().strip() for b in breadcrumb])

# Look at the main content
main_content = soup.select('.container, .main')
if main_content:
    content = main_content[0]
    print('Main content headings:')
    for h in content.select('h1, h2, h3, h4'):
        print(f'  {h.name}: {h.get_text().strip()}')