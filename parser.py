# HTML Parsing logic for the Advanced E-commerce Product Scraper

import logging
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Assuming utils.py and config.py are accessible
from . import utils
from . import config

# --- IMPORTANT --- 
# The CSS selectors used below are GENERIC EXAMPLES based on common e-commerce patterns.
# They MUST be adapted based on the specific HTML structure of the target website 
# (e.g., Amazon, Best Buy, etc.) identified in config.py.
# Use browser developer tools (Inspect Element) to find the correct selectors for your target site.

# --- Example Selectors (Adapt These!) ---
PRODUCT_CONTAINER_SELECTOR = "div.product-item" # Example: A container for each product
PRODUCT_NAME_SELECTOR = "h2.product-title a" # Example: Product name within an H2 tag inside a link
PRODUCT_PRICE_SELECTOR = "span.price" # Example: Price within a span with class 'price'
PRODUCT_RATING_SELECTOR = "div.rating span.star-rating" # Example: Rating text/value
PRODUCT_REVIEWS_SELECTOR = "a.reviews-link span" # Example: Number of reviews text
PRODUCT_URL_SELECTOR = "h2.product-title a[href]" # Example: URL from the product title link
NEXT_PAGE_SELECTOR = "a.pagination-next[href]" # Example: The 'Next' page link
# --- End Example Selectors ---

def parse_product_listings(html_content):
    """Parses the product listing page to extract individual product details.

    Args:
        html_content (str): The HTML content of the product listing page.

    Returns:
        list: A list of dictionaries, each containing details for a product found on the page.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    products_data = []
    product_containers = soup.select(PRODUCT_CONTAINER_SELECTOR)

    if not product_containers:
        logging.warning(f"Could not find product containers using selector: {PRODUCT_CONTAINER_SELECTOR}")
        # Add fallback selectors here if needed
        return []

    logging.info(f"Found {len(product_containers)} potential product containers on the page.")

    for container in product_containers:
        try:
            name_element = container.select_one(PRODUCT_NAME_SELECTOR)
            name = name_element.get_text(strip=True) if name_element else None

            price_element = container.select_one(PRODUCT_PRICE_SELECTOR)
            price_str = price_element.get_text(strip=True) if price_element else None
            price = utils.clean_price(price_str) # Use utility function for cleaning

            rating_element = container.select_one(PRODUCT_RATING_SELECTOR)
            # Rating extraction might need specific parsing (e.g., from class name, text, aria-label)
            rating_str = rating_element.get_text(strip=True) if rating_element else None 
            # Example: Try to extract a number like \"4.5\" or \"4.5 out of 5 stars\"
            rating_match = re.search(r"(\d+(\.\d+)?)", rating_str) if rating_str else None
            rating = float(rating_match.group(1)) if rating_match else None

            reviews_element = container.select_one(PRODUCT_REVIEWS_SELECTOR)
            reviews_str = reviews_element.get_text(strip=True) if reviews_element else None
            # Example: Try to extract a number, removing commas
            reviews_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+)", reviews_str) if reviews_str else None
            reviews = int(reviews_match.group(1).replace(",", "")) if reviews_match else None

            url_element = container.select_one(PRODUCT_URL_SELECTOR)
            relative_url = url_element["href"] if url_element and url_element.has_attr("href") else None
            # Construct absolute URL
            absolute_url = urljoin(config.BASE_URL, relative_url) if relative_url else None

            # Basic validation: Ensure at least name and URL are found
            if name and absolute_url:
                product_info = {
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "url": absolute_url,
                    "scraped_timestamp": utils.get_timestamp_string()
                }
                products_data.append(product_info)
            else:
                logging.debug(f"Skipping container due to missing name or URL. Selector: {PRODUCT_CONTAINER_SELECTOR}")

        except Exception as e:
            logging.warning(f"Error parsing a product container: {e}. Container snippet: {str(container)[:200]}...", exc_info=False)
            continue

    logging.info(f"Successfully parsed {len(products_data)} products from the page.")
    return products_data

def find_next_page_url(html_content):
    """Finds the URL for the next page of product listings.

    Args:
        html_content (str): The HTML content of the current product listing page.

    Returns:
        str or None: The absolute URL of the next page, or None if not found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    next_link_element = soup.select_one(NEXT_PAGE_SELECTOR)

    if next_link_element and next_link_element.has_attr("href"):
        next_href = next_link_element["href"]
        # Handle relative URLs
        absolute_next_url = urljoin(config.BASE_URL, next_href)
        logging.info(f"Found next page URL: {absolute_next_url}")
        return absolute_next_url
    else:
        logging.info(f"No next page link found using selector: {NEXT_PAGE_SELECTOR}")
        return None

# Placeholder for parsing detail pages if needed in the future
# def parse_product_details(html_content):
#     """Parses the detailed product description page.
#     Args:
#         html_content (str): The HTML content of the product details page.
#     Returns:
#         dict: A dictionary containing detailed product information.
#     """
#     soup = BeautifulSoup(html_content, "html.parser")
#     details = {}
#     # --- Add selectors and logic for detail page elements --- 
#     # Example: description_selector = "div#productDescription"
#     # description_element = soup.select_one(description_selector)
#     # details["full_description"] = description_element.get_text(strip=True) if description_element else None
#     logging.info("Parsed product details page.")
#     return details

