# Main entry point for the Advanced E-commerce Product Scraper

import logging
import sys
import os

# Ensure the src directory is discoverable for imports
# This allows running `python main.py` from the project root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Now import project modules
from src import utils
from src import config
from src.scraper import ProductScraper

def main():
    """Main execution function for the scraper."""
    # Setup logging first
    utils.setup_logging()
    logging.info(f"--- Advanced E-commerce Product Scraper Initialized ({config.TARGET_SITE_NAME}) ---")

    scraper_instance = None # Initialize for the finally block
    try:
        # Instantiate the scraper (which also sets up the WebDriver)
        scraper_instance = ProductScraper()

        # Run the scraping process
        scraped_data = scraper_instance.scrape_products()

        # Save the results if data was collected
        if scraped_data:
            logging.info(f"Total products scraped: {len(scraped_data)}. Saving results...")
            # Save to both CSV and JSON as configured
            utils.save_to_csv(scraped_data, config.OUTPUT_FILENAME_CSV)
            utils.save_to_json(scraped_data, config.OUTPUT_FILENAME_JSON)
            logging.info("Data saving complete.")
        else:
            logging.warning("No product data was scraped. Output files will not be created or will be empty. Check logs and selectors.")

    except Exception as e:
        # Catch any unhandled exceptions during the process
        logging.critical(f"An critical error occurred in the main execution: {e}", exc_info=True)
        # scraper_instance might be None if WebDriver setup failed

    finally:
        # Ensure the WebDriver is always closed
        if scraper_instance:
            scraper_instance.close_driver()
        logging.info(f"--- Advanced E-commerce Product Scraper Finished ({config.TARGET_SITE_NAME}) ---")

if __name__ == "__main__":
    # Check if running from within the src directory and adjust path if needed
    # This is less common; standard practice is to run from the project root.
    # if os.path.basename(os.getcwd()) == "src":
    #     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    #     # Re-import might be needed if modules were already loaded with wrong path context

    main()

