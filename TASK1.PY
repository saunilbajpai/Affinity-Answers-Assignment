"""
MDComputers Product Information Extractor

This script prompts the user for a search term, fetches the search results page
from MDComputers (https://mdcomputers.in/), parses the HTML response, and extracts
product names and selling prices.
"""

import sys
from urllib.parse import urlencode, urljoin
import requests
from bs4 import BeautifulSoup

# Fix Windows console UTF-8 output formatting for currency symbols like '₹'
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Target website configurations
BASE_URL = "https://mdcomputers.in/"
SEARCH_ROUTE = "product/search"
REQUEST_TIMEOUT_SECONDS = 10

# Full browser request headers to avoid HTTP 403 Forbidden errors caused by WAF/security checks
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# HTML Selectors (supports both updated and legacy MDComputers site layouts)
PRODUCT_CONTAINER_CLASSES = ["product-grid-item", "product-thumb", "product-layout"]
TITLE_CLASSES = ["product-entities-title", "name", "title"]


def build_search_url(search_term: str) -> str:
    """
    Construct the search results URL for MDComputers given a search term.

    Args:
        search_term (str): The search query string.

    Returns:
        str: Fully qualified URL.
    """
    query_string = urlencode({
        "route": SEARCH_ROUTE,
        "search": search_term.strip()
    })
    return urljoin(BASE_URL, f"?{query_string}")


def fetch_search_results_html(url: str) -> str:
    """
    Fetch raw HTML content from the given URL using HTTP GET.

    Args:
        url (str): The search URL to fetch.

    Returns:
        str: Raw HTML body.

    Raises:
        requests.RequestException: On network failures or HTTP errors.
    """
    response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.text


def extract_selling_price(price_container) -> str:
    """
    Extract the selling price from a product's price container.
    Handles discounted items (where an original price is strikethrough) and standard priced items.

    Args:
        price_container (Tag): BeautifulSoup element for the price block.

    Returns:
        str: Extracted price string (e.g. '₹9,290') or 'Price not available'.
    """
    if price_container is None:
        return "Price not available"

    # Check for discounted price tag (modern layout uses class 'ins', legacy uses 'price-new')
    discounted_tag = price_container.find(class_=["ins", "price-new"])
    if discounted_tag:
        price_text = discounted_tag.get_text(strip=True)
        if price_text:
            return price_text

    # If no discount tag, create a copy of price_container and strip old strikethrough prices
    price_copy = BeautifulSoup(str(price_container), "html.parser")
    for old_tag in price_copy.find_all(class_=["del", "price-old"]):
        old_tag.extract()

    price_text = price_copy.get_text(strip=True)
    return price_text if price_text else "Price not available"


def parse_products(html_content: str) -> list[dict[str, str]]:
    """
    Parse HTML search page to extract list of product names and selling prices.

    Args:
        html_content (str): HTML content of search results page.

    Returns:
        list[dict]: List of dictionaries containing 'name' and 'price'.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Try finding products using current and fallback container classes
    product_elements = []
    for cls in PRODUCT_CONTAINER_CLASSES:
        found = soup.find_all(class_=cls)
        if found:
            product_elements = found
            break

    products = []
    for element in product_elements:
        # Locate title
        title_element = element.find(class_=TITLE_CLASSES) or element.find("h3") or element.find("h4")
        if not title_element:
            continue
        
        name = title_element.get_text(strip=True)
        if not name:
            continue

        # Locate price block
        price_block = element.find(class_="price")
        price = extract_selling_price(price_block)

        products.append({"name": name, "price": price})

    return products


def display_products(products: list[dict[str, str]], search_term: str) -> None:
    """
    Display extracted products formatted cleanly in console output.

    Args:
        products (list[dict]): List of product records.
        search_term (str): Search term used.
    """
    if not products:
        print(f"\nNo products found for '{search_term}'.")
        return

    print(f"\nFound {len(products)} product(s) for '{search_term}':\n")
    header = f"{'#':<4} {'Product Name':<70} {'Selling Price'}"
    print(header)
    print("-" * len(header))

    for idx, item in enumerate(products, start=1):
        name = item["name"]
        truncated_name = (name[:66] + "...") if len(name) > 69 else name
        print(f"{idx:<4} {truncated_name:<70} {item['price']}")


def main() -> None:
    """Main execution function."""
    try:
        search_term = input("Enter search term: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        return

    if not search_term:
        print("Error: Search term cannot be empty.")
        sys.exit(1)

    search_url = build_search_url(search_term)
    print(f"\nFetching search results from: {search_url} ...")

    try:
        html = fetch_search_results_html(search_url)
    except requests.HTTPError as err:
        print(f"\nHTTP Error occurred: {err}")
        sys.exit(1)
    except requests.RequestException as err:
        print(f"\nFailed to retrieve search results: {err}")
        sys.exit(1)

    products = parse_products(html)
    display_products(products, search_term)


if __name__ == "__main__":
    main()