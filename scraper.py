#!/usr/bin/env python3
"""
Web Scraper for Login Elements

This script fetches a webpage, identifies login form elements,
and extracts them for analysis. Designed for beginners learning Python.

Usage: python scraper.py <URL>
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class ScraperError(Exception):
    """Base exception for scraper errors."""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code or "SCRAPER_ERROR"


class InvalidURLError(ScraperError):
    """Exception raised for invalid URLs."""
    def __init__(self, url):
        super().__init__(f"Invalid URL: {url}", "INVALID_URL")


class FetchError(ScraperError):
    """Exception raised when fetching page content fails."""
    def __init__(self, url, reason):
        super().__init__(f"Failed to fetch content from {url}: {reason}", "FETCH_ERROR")


class ParseError(ScraperError):
    """Exception raised when parsing HTML fails."""
    def __init__(self, reason):
        super().__init__(f"Failed to parse HTML: {reason}", "PARSE_ERROR")


class NoLoginElementsError(ScraperError):
    """Exception raised when no login elements are found."""
    def __init__(self, url):
        super().__init__(f"No login elements found on {url}", "NO_LOGIN_ELEMENTS")


def validate_url(url):
    """
    Validate if the provided URL is a valid HTTP or HTTPS URL.
    If missing protocol, automatically add 'https://'.

    Args:
        url (str): The URL to validate

    Returns:
        str: The validated URL with protocol

    Raises:
        InvalidURLError: If the URL is invalid
    """
    try:
        # If no scheme, add https://
        if '://' not in url:
            url = 'https://' + url
        parsed = urlparse(url)
        if parsed.scheme in ['http', 'https'] and bool(parsed.netloc):
            return url
        raise InvalidURLError(url)
    except Exception:
        raise InvalidURLError(url)


def fetch_page_content(url, use_selenium=False):
    """
    Fetch the HTML content of a webpage.

    Args:
        url (str): The URL to fetch
        use_selenium (bool): Whether to use Selenium for dynamic content

    Returns:
        str: The HTML content

    Raises:
        FetchError: If fetching the content fails
    """
    try:
        if use_selenium:
            # Set up headless Chrome for dynamic content
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            # Wait a bit for JavaScript to load
            driver.implicitly_wait(5)

            html = driver.page_source
            driver.quit()
            return html
        else:
            # Use requests for static content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text

    except requests.exceptions.RequestException as e:
        raise FetchError(url, str(e))
    except Exception as e:
        raise FetchError(url, str(e))


def parse_html(html_content):
    """
    Parse HTML content into a BeautifulSoup object.

    Args:
        html_content (str): The HTML content to parse

    Returns:
        BeautifulSoup: Parsed HTML object

    Raises:
        ParseError: If parsing fails
    """
    try:
        return BeautifulSoup(html_content, 'html.parser')
    except Exception as e:
        raise ParseError(str(e))


def find_login_elements(soup):
    """
    Search for login-related elements in the parsed HTML.

    Args:
        soup (BeautifulSoup): Parsed HTML object

    Returns:
        list: List of dictionaries containing found elements

    Raises:
        NoLoginElementsError: If no login elements are found
    """
    login_elements = []

    # High-confidence selectors
    password_selectors = [
        'input[type="password"]',
        'input[autocomplete="current-password"]'
    ]

    username_selectors = [
        'input[name*="user"]',
        'input[name*="email"]',
        'input[name*="username"]',
        'input[id*="user"]',
        'input[id*="email"]',
        'input[id*="username"]',
        'input[autocomplete="username"]',
        'input[autocomplete="email"]'
    ]

    # Find password inputs
    for selector in password_selectors:
        elements = soup.select(selector)
        for element in elements:
            login_elements.append({
                'type': 'password',
                'element': element,
                'html': str(element)
            })

    # Find username inputs
    for selector in username_selectors:
        elements = soup.select(selector)
        for element in elements:
            # Avoid duplicates if already found as password
            if element not in [item['element'] for item in login_elements]:
                login_elements.append({
                    'type': 'username',
                    'element': element,
                    'html': str(element)
                })

    if not login_elements:
        raise NoLoginElementsError("")

    return login_elements


def save_to_json(data, filename='login_elements.json'):
    """
    Save extracted data to a JSON file.

    Args:
        data (list): List of dictionaries to save
        filename (str): Name of the JSON file
    """
    try:
        # Load existing data if file exists
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # Add new data
        existing_data.extend(data)

        # Save back to file
        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=2, default=str)

        print(f"Data saved to {filename}")

    except Exception as e:
        print(f"Error saving data: {e}")


def main():
    """
    Main function to run the web scraper.
    """
    parser = argparse.ArgumentParser(description='Extract login elements from a webpage')
    parser.add_argument('url', help='URL of the webpage to scrape')

    args = parser.parse_args()

    url = args.url

    try:
        # Validate URL
        url = validate_url(url)

        print(f"Fetching content from: {url}")

        # Fetch page content - start with static
        html_content = fetch_page_content(url, False)

        # Parse HTML
        soup = parse_html(html_content)

        # Find login elements
        login_elements = find_login_elements(soup)

        # If no login elements found with static scraping, try with Selenium
        if not login_elements:
            print("No login elements found with static scraping. Retrying with Selenium...")
            html_content = fetch_page_content(url, True)
            soup = parse_html(html_content)
            login_elements = find_login_elements(soup)

        print(f"Found {len(login_elements)} login element(s)")

        # Prepare data for storage
        timestamp = datetime.now(timezone.utc).isoformat()
        data_to_save = []

        for element in login_elements:
            data_to_save.append({
                'url': url,
                'field_type': element['type'],
                'extracted_html': element['html'],
                'timestamp': timestamp
            })

        # Save to JSON
        save_to_json(data_to_save)

        # Print results
        print("\nExtracted elements:")
        for item in data_to_save:
            print(f"- {item['field_type']}: {item['extracted_html'][:100]}...")

    except InvalidURLError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except FetchError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ParseError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except NoLoginElementsError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()