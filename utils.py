# Utility functions for the Advanced E-commerce Product Scraper

import logging
import os
import pandas as pd
import json
import re
from datetime import datetime

# Assuming config.py is in the same directory or path is handled
from . import config

def setup_logging():
    """Sets up the logging configuration."""
    # Construct absolute path for log directory relative to this file's location
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), config.LOG_DIR))
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, config.LOG_FILENAME)

    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)

    # Remove existing handlers to avoid duplicate logs if function is called multiple times
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s",
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler() # Also print logs to console
        ]
    )
    logging.info(f"Logging setup complete. Log level: {config.LOG_LEVEL}. Log file: {log_filepath}")

def save_to_csv(data, filename):
    """Saves the scraped data to a CSV file.

    Args:
        data (list): A list of dictionaries, where each dictionary represents a product.
        filename (str): The name of the output CSV file.
    """
    if not data:
        logging.warning("No data provided to save to CSV.")
        return

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), config.OUTPUT_DIR))
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    try:
        df = pd.DataFrame(data)
        # Ensure consistent column order if needed, based on expected fields
        # expected_columns = ['name', 'price', 'rating', 'reviews', 'url', 'scraped_timestamp']
        # df = df.reindex(columns=expected_columns)
        df.to_csv(filepath, index=False, encoding='utf-8')
        logging.info(f"Data successfully saved to CSV: {filepath}")
    except Exception as e:
        logging.error(f"Error saving data to CSV {filepath}: {e}", exc_info=True)

def save_to_json(data, filename):
    """Saves the scraped data to a JSON file.

    Args:
        data (list): A list of dictionaries, where each dictionary represents a product.
        filename (str): The name of the output JSON file.
    """
    if not data:
        logging.warning("No data provided to save to JSON.")
        return

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), config.OUTPUT_DIR))
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Data successfully saved to JSON: {filepath}")
    except Exception as e:
        logging.error(f"Error saving data to JSON {filepath}: {e}", exc_info=True)

def clean_price(price_str):
    """Cleans a price string to extract a float value.

    Handles common currency symbols, commas, and ranges.
    Returns the cleaned price as a float, or None if cleaning fails.
    """
    if price_str is None:
        return None
    try:
        # Remove currency symbols ($, £, €, etc.), commas, and whitespace
        cleaned = re.sub(r"[$,£€]|\s|,|", "", str(price_str).strip())
        # Handle price ranges (e.g., "100-200"), take the lower value
        if '-' in cleaned:
            cleaned = cleaned.split('-')[0]
        # Handle 'Free'
        if cleaned.lower() == 'free':
            return 0.0
        # Convert to float
        price = float(cleaned)
        return price
    except (ValueError, TypeError) as e:
        logging.debug(f"Could not clean price string: '{price_str}'. Error: {e}")
        return None # Return None if conversion fails

def get_timestamp_string():
    """Returns the current timestamp as an ISO 8601 formatted string."""
    return datetime.now().isoformat()

# Example usage within the project:
# timestamp = utils.get_timestamp_string()
# product_data['scraped_timestamp'] = timestamp

