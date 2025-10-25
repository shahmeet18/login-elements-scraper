# Web Scraper for Login Elements

A comprehensive web scraping tool that fetches webpage content, identifies login form elements, and extracts them for analysis. Supports CLI usage, REST API, and web interface.

## Features

- **URL Validation**: Checks for valid HTTP/HTTPS URLs
- **Static Content**: Uses `requests` for regular web pages
- **Dynamic Content**: Optional Selenium support for Single Page Applications (SPAs)
- **Login Detection**: Identifies password and username input fields
- **Data Storage**: Saves extracted elements to JSON file
- **Multiple Interfaces**: Command Line Interface, REST API, and Web Interface

## Installation

1. Install Python 3.7+ if you haven't already
2. Clone or download this project
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

#### Basic Usage (Static Pages)

```bash
python scraper.py https://example.com/login
```

#### For Dynamic/SPA Pages

```bash
python scraper.py https://example.com/login --selenium
```

### REST API

The application includes a FastAPI-based REST API for programmatic access.

#### Starting the API Server

```bash
python app.py
```

Or use the provided run script:

```bash
./run.sh
```

The API will be available at `http://localhost:8000`

#### API Endpoints

**POST /scrape**
Scrape login elements from a given URL.

Request body:
```json
{
  "url": "https://example.com/login",
  "use_selenium": false
}
```

Response:
```json
{
  "url": "https://example.com/login",
  "login_elements": [
    {
      "type": "username",
      "html": "<input type=\"text\" name=\"username\" id=\"user\" ...>"
    },
    {
      "type": "password",
      "html": "<input type=\"password\" name=\"password\" id=\"pass\" ...>"
    }
  ],
  "count": 2
}
```

#### API Usage Examples

Using curl:
```bash
curl -X POST "http://localhost:8000/scrape" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/login", "use_selenium": false}'
```

Using Python requests:
```python
import requests

response = requests.post("http://localhost:8000/scrape", json={
    "url": "https://example.com/login",
    "use_selenium": False
})
print(response.json())
```

### Web Interface

The application includes a web-based interface for easy interaction.

#### Starting the Web Interface

```bash
python app.py
```

Or use the provided run script:

```bash
./run.sh
```

#### Using the Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter the URL you want to scrape in the input field
3. Check the "Use Selenium" box if the page is dynamic/SPA
4. Click "Scrape Login Elements"
5. View the results displayed on the page

## Output

The script will:
1. Fetch the webpage content
2. Search for login-related input fields
3. Save found elements to `login_elements.json`
4. Display results in the terminal

## Example Output

```json
[
  {
    "url": "https://example.com/login",
    "field_type": "username",
    "extracted_html": "<input type=\"text\" name=\"username\" id=\"user\" ...>",
    "timestamp": "2025-10-25T02:56:29.536Z"
  },
  {
    "url": "https://example.com/login",
    "field_type": "password",
    "extracted_html": "<input type=\"password\" name=\"password\" id=\"pass\" ...>",
    "timestamp": "2025-10-25T02:56:29.536Z"
  }
]
```

## How It Works

1. **URL Validation**: Ensures the provided URL is valid
2. **Content Fetching**: Downloads the HTML content
   - Static pages: Uses `requests` library
   - Dynamic pages: Uses Selenium with headless Chrome
3. **HTML Parsing**: Converts HTML to searchable DOM tree using BeautifulSoup
4. **Element Detection**: Searches for login inputs using CSS selectors
5. **Data Extraction**: Gets the outer HTML of found elements
6. **Storage**: Saves structured data to JSON file

## Dependencies

- `requests`: For HTTP requests
- `beautifulsoup4`: For HTML parsing
- `selenium`: For dynamic content (optional)
- `webdriver-manager`: For automatic Chrome driver management
- `fastapi`: For building the REST API
- `uvicorn`: For running the FastAPI application
- `pydantic`: For data validation and serialization

## Learning Resources

- [Python Requests Documentation](https://requests.readthedocs.io/)
- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)

## Troubleshooting

- **Chrome Driver Issues**: Make sure Chrome is installed for Selenium mode
- **Network Errors**: Check your internet connection and URL validity
- **No Elements Found**: Try using `--selenium` flag for dynamic pages

## License

This project is for educational purposes. Please respect website terms of service and robots.txt files.