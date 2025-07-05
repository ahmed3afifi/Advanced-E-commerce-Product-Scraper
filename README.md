# Advanced E-commerce Product Scraper

## Overview

This project implements an advanced web scraper designed to extract product information from e-commerce websites. It navigates category or search result pages, scrapes key details for listed products (e.g., name, price, rating, review count, URL), handles pagination, and saves the collected data into structured formats (CSV and JSON).

Built using Python, Selenium, and BeautifulSoup, this scraper demonstrates techniques for handling dynamic content, parsing complex HTML structures typical of e-commerce sites, managing configuration, implementing robust error handling, and logging. It serves as a strong portfolio piece showcasing practical skills in web data extraction for market analysis, price monitoring, or competitive research.

**Disclaimer**: Web scraping can be against the Terms of Service of many e-commerce websites. Always review the target site's `robots.txt` file and Terms of Service before running this scraper. Scrape responsibly, ethically, and avoid overloading the website's servers. The selectors provided are examples and **must** be adapted to the specific structure of the target website.

## Features

*   **Target Adaptability**: Designed with configuration for easy adaptation to different e-commerce sites (requires updating selectors in `parser.py`).
*   **Dynamic Content Handling**: Utilizes Selenium WebDriver to render JavaScript and handle elements loaded dynamically after the initial page load.
*   **Pagination Navigation**: Automatically iterates through multiple pages of product listings based on configuration or until no 'Next' page link is found.
*   **Robust HTML Parsing**: Employs BeautifulSoup4 with CSS selectors to extract product data. Includes examples for common data points (name, price, rating, reviews, URL).
*   **Data Cleaning**: Includes utility functions (e.g., `clean_price`) to standardize extracted data like prices.
*   **Structured Output**: Saves scraped data into well-formatted CSV and JSON files via Pandas and the `json` library.
*   **Configuration Management**: Centralized settings in `src/config.py` for target site URL, category/search path, scraping depth, output files, logging level, browser options (headless), and request delays.
*   **Modular Architecture**: Codebase is organized into logical modules (`scraper.py`, `parser.py`, `utils.py`, `config.py`, `main.py`) promoting maintainability and readability.
*   **Error Handling & Logging**: Incorporates `try-except` blocks for common scraping exceptions (timeouts, element not found, WebDriver issues) and detailed logging (to console and file `logs/ecommerce_scraper.log`) for monitoring and debugging.
*   **Dependency Management**: Provides a `requirements.txt` file for easy environment setup.
*   **Anti-Detection Techniques (Basic)**: Includes user-agent string customization and optional settings (disabling automation flags) to reduce the likelihood of being blocked.

## Technology Stack

*   **Language**: Python 3
*   **Web Automation/Interaction**: Selenium
*   **WebDriver Management**: webdriver-manager
*   **HTML/XML Parsing**: BeautifulSoup4
*   **Data Manipulation**: Pandas
*   **Standard Libraries**: `logging`, `os`, `json`, `re`, `time`, `urllib.parse`

## Project Structure

```
ecommerce_scraper/
├── data/                 # Directory for storing output CSV and JSON files
├── logs/                 # Directory for storing log files
├── src/
│   ├── __init__.py       # Makes src a Python package
│   ├── config.py         # Scraper configuration settings
│   ├── parser.py         # HTML parsing functions and selectors (NEEDS ADAPTATION)
│   ├── scraper.py        # Core scraping class using Selenium
│   ├── utils.py          # Helper functions (logging, saving, cleaning)
│   └── (WebDriver files) # Potentially downloaded by webdriver-manager
├── main.py               # Main script to run the scraper
├── requirements.txt      # List of Python dependencies
└── README.md             # This documentation file
```

## Setup and Installation

1.  **Clone or Download**: Obtain the project files.
    ```bash
    # Example using Git
    git clone <repository_url>
    cd ecommerce_scraper
    ```
    Alternatively, download and extract the project ZIP file.

2.  **Create Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    # Activate:
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```

3.  **Install Dependencies**: Ensure Python 3 and pip are installed. Run:
    ```bash
    pip install -r requirements.txt
    ```
    This installs Selenium, webdriver-manager, BeautifulSoup4, Pandas, and requests.

4.  **Install Google Chrome**: The scraper uses ChromeDriver, managed by `webdriver-manager`. You must have the Google Chrome browser installed on your system.

## Configuration (Crucial Step)

Before running the scraper, you **must** configure it for your target e-commerce website by editing `src/config.py` and `src/parser.py`:

1.  **`src/config.py`**: 
    *   Set `TARGET_SITE_NAME` (e.g., "Noon", "Amazon").
    *   Set `BASE_URL` to the correct base URL of the target site.
    *   Set `CATEGORY_PATH` to the specific category or search results path you want to scrape.
    *   Adjust `MAX_PAGES`, `OUTPUT_DIR`, `LOG_LEVEL`, `HEADLESS_BROWSE`, `REQUEST_DELAY` as needed.

2.  **`src/parser.py`**: 
    *   **This is the most critical adaptation step.** Use your browser's developer tools (right-click -> Inspect Element) on the target website's category/search results page.
    *   Identify the correct CSS selectors for:
        *   The main container holding each product (`PRODUCT_CONTAINER_SELECTOR`).
        *   The product name (`PRODUCT_NAME_SELECTOR`).
        *   The product price (`PRODUCT_PRICE_SELECTOR`).
        *   The product rating (`PRODUCT_RATING_SELECTOR`).
        *   The number of reviews (`PRODUCT_REVIEWS_SELECTOR`).
        *   The product URL (`PRODUCT_URL_SELECTOR`).
        *   The 'Next' page link/button (`NEXT_PAGE_SELECTOR`).
    *   Update the placeholder selectors at the top of `src/parser.py` with the correct ones you found.
    *   You may also need to adjust the parsing logic within the `parse_product_listings` function if the data format requires specific cleaning or extraction methods (e.g., extracting rating from a class name like `a-star-4-5`).

## Usage

Once configured and dependencies are installed:

1.  Navigate to the project's root directory (`ecommerce_scraper/`) in your terminal.
2.  Ensure your virtual environment (if created) is activated.
3.  Run the main script:
    ```bash
    python main.py
    ```

The scraper will:
*   Initialize logging.
*   Set up the Selenium WebDriver (potentially downloading ChromeDriver).
*   Navigate to the starting category/search URL.
*   Iterate through the specified number of pages (or until no 'Next' page is found).
*   Parse product data using the selectors you configured.
*   Save the results to `data/products.csv` and `data/products.json`.
*   Log progress and errors to the console and `logs/ecommerce_scraper.log`.
*   Close the WebDriver.

## Code Explanation

*   **`main.py`**: Entry point. Sets up logging, creates `ProductScraper`, runs scraping, saves data via `utils`, handles top-level errors, ensures driver cleanup.
*   **`scraper.py`**: Defines `ProductScraper` class. Manages WebDriver lifecycle, browser navigation (fetching URLs, handling timeouts), retrieves page source, orchestrates calls to `parser` for data extraction and pagination link finding, implements request delays.
*   **`parser.py`**: Contains functions (`parse_product_listings`, `find_next_page_url`) using BeautifulSoup to parse HTML. **Requires site-specific CSS selectors.** Extracts product attributes and the next page URL.
*   **`utils.py`**: Provides helper functions: `setup_logging`, `save_to_csv`, `save_to_json`, `clean_price`, `get_timestamp_string`.
*   **`config.py`**: Central repository for all configuration parameters.

## Potential Improvements / Future Work

*   **Detailed Product Page Scraping**: Extend functionality to visit individual product URLs and scrape more details (e.g., full description, specifications, seller information).
*   **Handling Variations**: Parse product variations (size, color) if present.
*   **Proxy Integration**: Add support for using proxies (rotating proxies recommended for larger scrapes) to avoid IP blocks.
*   **CAPTCHA Handling**: Integrate services or techniques to handle CAPTCHAs (can be complex).
*   **Database Storage**: Save data to a database (SQLite, PostgreSQL, MongoDB) for more robust storage and querying.
*   **Asynchronous Operations**: Explore `asyncio` with libraries like `Playwright` or `httpx` + `BeautifulSoup` for potentially faster scraping (more complex implementation).
*   **Delta Scraping**: Implement logic to only scrape new or updated products since the last run.
*   **More Sophisticated Anti-Detection**: Implement more advanced browser fingerprinting countermeasures.


