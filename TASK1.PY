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