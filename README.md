# E-commerce Web Scraper

A Python-based web scraper for extracting product data from e-commerce static test sites using Beautiful Soup.

## Project Purpose

This project demonstrates a complete web scraping solution that navigates through:
- Categories
- Subcategories
- Paginated product listing pages
- Individual product detail pages

The scraper extracts comprehensive product information and generates structured CSV outputs for analysis.

## Setup Instructions

### Prerequisites
- Python 3.14 or higher
- uv package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-scraper
```

2. Install dependencies using uv:
```bash
uv sync
```

This will create a virtual environment and install all required packages.

## Usage

### Running the Scraper

To run the complete scraping workflow:

```bash
uv run python src/main.py
```

The scraper will:
1. Discover all categories and subcategories
2. Navigate through paginated listing pages
3. Extract detailed product information
4. Generate CSV output files

### Output Files

The scraper generates two CSV files in the `data/` directory:

- `products.csv`: Complete product-level dataset
- `category_summary.csv`: Summary statistics by subcategory

## Branch Workflow

This project follows Git Flow branching strategy:

1. **main**: Production-ready code
2. **dev**: Development integration branch
3. **feature/catalog-navigation**: Category and subcategory discovery
4. **feature/product-details**: Product detail page parsing
5. **fix/url-resolution**: URL joining and resolution fixes
6. **fix/deduplication**: Duplicate product removal

### Workflow Steps
1. Created repository with `main` branch
2. Created `dev` branch from `main`
3. Created `feature/catalog-navigation` for navigation logic
4. Created `feature/product-details` for product parsing
5. Merged both features into `dev`
6. Created `fix/url-resolution` for URL handling
7. Created `fix/deduplication` for data cleaning
8. Merged fixes into `dev`
9. Final merge of `dev` into `main`

## Dependencies

- `requests>=2.31.0`: HTTP client for web requests
- `beautifulsoup4>=4.12.0`: HTML parsing library

## Project Structure

```
ecommerce-scraper/
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # This file
├── src/
│   ├── main.py           # Entry point
│   └── scraper/
│       ├── __init__.py
│       ├── crawler.py    # Navigation and URL discovery
│       ├── parsers.py    # Data extraction from pages
│       ├── exporters.py  # CSV generation
│       └── utils.py      # Helper functions
├── data/                 # Generated CSV outputs
│   ├── products.csv
│   └── category_summary.csv
└── tests/                # Test cases
```

## Data Extraction

### Product Data Fields
- Category and subcategory
- Product title
- Price (normalized to numeric)
- Product URL
- Image URL
- Description
- Review count/rating information
- Product specifications
- Page reference

### Data Processing
- URL resolution for relative links
- Price normalization (handles various formats)
- Text cleaning and whitespace removal
- Duplicate product removal
- Missing data handling

## Assumptions

- Target website structure remains consistent with the test site
- Rate limiting is implemented to be respectful to servers
- Product pages contain expected HTML structure
- Network connectivity is stable during scraping

## Limitations

- Designed specifically for the webscraper.io test site structure
- Does not handle JavaScript-rendered content
- Rate limiting may need adjustment for different sites
- Error handling focuses on common HTTP and parsing issues
- No authentication or session management for protected sites

## Technical Details

### Scraping Strategy
1. **Category Discovery**: Parse main page for category links
2. **Subcategory Navigation**: Extract subcategory links from category pages
3. **Pagination Handling**: Follow page links to collect all products
4. **Detail Extraction**: Visit each product page for complete information
5. **Data Cleaning**: Normalize and deduplicate extracted data
6. **Export**: Generate structured CSV files for analysis

### Error Handling
- Graceful handling of network failures
- Missing element protection
- Invalid data format handling
- Logging of scraping progress and errors

## Testing

Run tests with:
```bash
uv run python -m pytest tests/
```

## License

This project is for educational purposes.