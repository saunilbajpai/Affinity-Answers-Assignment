"""
Scrapes the first page of MDComputers search results
and prints product names and selling prices.
"""


import sys
from urllib.parse import urlencode, urljoin
 
import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# if MDComputers changes its URL scheme or theme,
# only this block needs to change.
# ---------------------------------------------------------------------------


BASE_URL = "https://mdcomputers.in/"
SEARCH_ROUTE = "product/search"
REQUEST_TIMEOUT_SECONDS = 10
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 ..."
}


# HTML selectors used by the product listing.
PRODUCT_CONTAINER_CLASS = "product-thumb"
PRODUCT_NAME_TAG = "h4"
PRICE_CONTAINER_CLASS = "price"
PRICE_NEW_CLASS = "price-new"
PRICE_OLD_CLASS = "price-old"


def build_search_url(search_term: str) -> str:

    """Build the MDComputers search-results URL for a given search term.
 
    Args:
        search_term: Free-text term the user wants to search for.
 
    Returns:
        A fully-qualified URL pointing at the search-results page.
    """

    query_string = urlencode({
        "route": SEARCH_ROUTE,
        "search": search_term
    })

    return urljoin(BASE_URL, "?" + query_string)


def fetch_search_results_html(url: str) -> str:
    """Retrieve the raw HTML of a search-results page.
 
    Args:
        url: The search URL to fetch.
 
    Returns:
        The response body as text.
 
    Raises:
        requests.RequestException: If the page cannot be retrieved
            (network error, timeout, non-2xx status code, etc).
    """
    response = requests.get(
        url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS
    )
    response.raise_for_status()
    return response.text


def _extract_selling_price(product_element) -> str:

    """Pull the selling (currently payable) price out of one product block.
 
    MDComputers shows a strikethrough original price alongside a
    discounted price for items on sale. When both are present we want the
    discounted one, since that's what the customer actually pays. When an
    item has no discount, only a single price is shown and we fall back
    to that.
 
    Args:
        product_element: A BeautifulSoup Tag representing one product card.
 
    Returns:
        The selling price as a string (e.g. "₹9,290"), or
        "Price not available" if no price could be located.
    """

    price_block = product_element.find(class_=PRICE_CONTAINER_CLASS)
    if price_block is None:
        return "Price not available"
 
    discounted_price = price_block.find(class_=PRICE_NEW_CLASS)
    if discounted_price is not None:
        return discounted_price.get_text(strip=True)
 
    # No discount badge present - the block should contain a single price,
    # but strip out any stray "price-old" node defensively before reading
    # the text, in case the theme still nests one.
    old_price = price_block.find(class_=PRICE_OLD_CLASS)
    if old_price is not None:
        old_price.extract()
 
    price_text = price_block.get_text(strip=True)
    return price_text if price_text else "Price not available"