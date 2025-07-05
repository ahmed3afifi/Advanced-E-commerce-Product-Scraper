# Core scraping logic for the Advanced E-commerce Product Scraper

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

# Assuming config, parser, utils are accessible
from . import config
from . import parser
from . import utils

class ProductScraper:
    """Manages the process of scraping product data using Selenium."""

    def __init__(self):
        """Initializes the ProductScraper with WebDriver setup."""
        self.driver = self._setup_driver()
        self.all_products_data = []

    def _setup_driver(self):
        """Sets up the Selenium WebDriver using webdriver-manager."""
        logging.info("Setting up WebDriver...")
        chrome_options = Options()
        if config.HEADLESS_BROWSE:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={config.USER_AGENT}")
        # Optional: Disable images to speed up loading
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        # Optional: Experimental options to potentially reduce detection
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        try:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            # Optional: Execute script to prevent detection
            # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            #     "source": """
            #         Object.defineProperty(navigator, \'webdriver\", {
            #           get: () => undefined
            #         })
            #     """
            # })
            logging.info("WebDriver setup successful.")
            return driver
        except WebDriverException as e:
            logging.error(f"Failed to initialize WebDriver: {e}", exc_info=True)
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred during WebDriver setup: {e}", exc_info=True)
            raise

    def _get_full_url(self, path):
        """Constructs the full URL from the base URL and a path."""
        return urljoin(config.BASE_URL, path)

    def scrape_products(self):
        """Main function to scrape product listings across multiple pages."""
        start_url = self._get_full_url(config.CATEGORY_PATH)
        logging.info(f"Starting product scraping for category: {config.CATEGORY_PATH} at {config.TARGET_SITE_NAME}")
        logging.info(f"Initial URL: {start_url}")

        current_url = start_url
        page_count = 0

        while current_url and page_count < config.MAX_PAGES:
            page_count += 1
            logging.info(f"Scraping page {page_count}: {current_url}")

            try:
                self.driver.get(current_url)
                # Wait for a key element of the product listing to be present
                # Adapt the selector based on the target site
                wait = WebDriverWait(self.driver, config.ELEMENT_WAIT_TIMEOUT)
                try:
                    # Example wait condition - adjust selector!
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, parser.PRODUCT_CONTAINER_SELECTOR)))
                    logging.debug(f"Product container element found using selector: {parser.PRODUCT_CONTAINER_SELECTOR}")
                except TimeoutException:
                    logging.warning(f"Timeout waiting for product containers on page {page_count}. Selector: {parser.PRODUCT_CONTAINER_SELECTOR}. Page might be empty or structure changed.")
                    # Check if it looks like a valid page anyway, maybe no products listed
                    if "no results" in self.driver.page_source.lower():
                         logging.info("Page indicates no results found. Stopping pagination.")
                         break
                    # Otherwise, continue to try parsing, but log the warning

                # Optional: Add a small delay after waiting, sometimes helps with JS rendering
                time.sleep(config.REQUEST_DELAY / 2)

                html_content = self.driver.page_source
                if not html_content:
                    logging.warning(f"Failed to retrieve HTML content for page {page_count} ({current_url}). Skipping page.")
                    # Try to find next page URL even if content retrieval failed partially
                    try:
                        current_url = parser.find_next_page_url(self.driver.page_source) # Try parsing again just for next link
                    except Exception:
                        current_url = None # Stop if we can't even find next link
                    continue

                page_products = parser.parse_product_listings(html_content)
                if not page_products and page_count == 1:
                    logging.warning("No products found on the first page. Check selectors in parser.py and config.py against the target website structure.")
                    # Optionally break if first page failure is critical
                    # break
                elif not page_products:
                    logging.info(f"No products found on page {page_count}. This might indicate the end of results.")
                    # Continue to check for a next page link, might be an empty page before the end.

                self.all_products_data.extend(page_products)
                logging.info(f"Found {len(page_products)} products on page {page_count}. Total products collected: {len(self.all_products_data)}")

                # Find the next page URL
                current_url = parser.find_next_page_url(html_content)
                if current_url:
                    logging.debug(f"Found next page link: {current_url}")
                    time.sleep(config.REQUEST_DELAY) # Delay before loading next page
                else:
                    logging.info("No further next page link found. Ending scraping.")
                    break

            except TimeoutException:
                logging.warning(f"Page load timed out for {current_url}. Skipping page {page_count}.")
                # Attempt to find next page URL from potentially incomplete source
                try:
                    current_url = parser.find_next_page_url(self.driver.page_source)
                except Exception:
                    logging.error("Failed to find next page link after timeout. Stopping.")
                    current_url = None
                continue
            except WebDriverException as e:
                logging.error(f"WebDriver error on page {page_count} ({current_url}): {e}", exc_info=True)
                # Decide whether to stop or try to continue
                break # Stop on significant WebDriver errors
            except Exception as e:
                logging.error(f"An unexpected error occurred while scraping page {page_count} ({current_url}): {e}", exc_info=True)
                # Try to find next page URL and continue if possible
                try:
                    current_url = parser.find_next_page_url(self.driver.page_source)
                except Exception:
                     logging.error("Failed to find next page link after unexpected error. Stopping.")
                     current_url = None
                continue

        if page_count >= config.MAX_PAGES:
            logging.info(f"Reached maximum page limit ({config.MAX_PAGES}). Stopping scraping.")

        logging.info(f"Scraping finished. Total products collected: {len(self.all_products_data)}")
        return self.all_products_data

    def close_driver(self):
        """Closes the Selenium WebDriver session."""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("WebDriver closed successfully.")
            except Exception as e:
                logging.error(f"Error closing WebDriver: {e}", exc_info=True)
            finally:
                self.driver = None

