# Configuration settings for the Advanced E-commerce Product Scraper

# --- Target Website Configuration ---
# IMPORTANT: Choose a specific target site and update BASE_URL and selectors in parser.py
# Example placeholder for a generic e-commerce site structure.
# Scraping sites like Amazon requires careful handling of their structure and anti-scraping measures.
# Always check the website's robots.txt and Terms of Service before scraping.
TARGET_SITE_NAME = "Noon" # e.g., "Amazon", "BestBuy", "Noon"
BASE_URL = "https://www.example-ecommerce.com" # Replace with actual base URL

# --- Search/Category Configuration ---
# Example: Scraping laptops category
CATEGORY_PATH = "/electronics/laptops" # Replace with the actual category path or search query structure
# Alternatively, use search query parameters if applicable
# SEARCH_QUERY = "gaming laptop"

# --- Scraping Parameters ---
# Number of pages of product listings to scrape
MAX_PAGES = 2 # Adjust as needed

# --- Output File Configuration ---
OUTPUT_DIR = "../data"
OUTPUT_FILENAME_CSV = "products.csv"
OUTPUT_FILENAME_JSON = "products.json"

# --- Logging Configuration ---
LOG_DIR = "../logs"
LOG_FILENAME = "ecommerce_scraper.log"
LOG_LEVEL = "INFO" # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# --- Selenium/WebDriver Settings ---
# Set to True to run the browser in headless mode (without GUI)
HEADLESS_BROWSE = True
# Timeouts (in seconds)
PAGE_LOAD_TIMEOUT = 45 # Increased timeout for potentially heavier e-commerce pages
ELEMENT_WAIT_TIMEOUT = 15 # Increased wait time for dynamic elements

# --- Request Handling ---
# Delay between requests (in seconds) to avoid overwhelming the server
REQUEST_DELAY = 3 # Be polite, especially to e-commerce sites
# User agent string to mimic a real browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"

