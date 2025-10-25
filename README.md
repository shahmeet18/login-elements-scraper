# Web Scraper for Login Elements

A comprehensive web scraping tool that fetches webpage content, identifies login form elements, and extracts them for analysis. Supports CLI usage, REST API, and web interface.

## Quick Start - Web Interface

The easiest way to use the application is through the web interface:

1. **Start the server**:
   ```bash
   python app.py
   # or
   ./run.sh
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Enter a URL** in the input field or click on one of the example tags

4. **Click "Scrape Login Elements"** - the tool automatically handles both static and dynamic pages

5. **View results** displayed on the page and copy the JSON using the "Copy JSON" button

## Features

- **URL Validation**: Checks for valid HTTP/HTTPS URLs and automatically adds https:// if missing
- **Static Content**: Uses `requests` for regular web pages
- **Dynamic Content**: Automatic fallback to Selenium for Single Page Applications (SPAs) when static scraping fails
- **Login Detection**: Identifies password and username input fields using comprehensive CSS selectors
- **Data Storage**: Saves extracted elements to JSON file (CLI mode only)
- **Multiple Interfaces**: Command Line Interface, REST API, and Web Interface
- **Error Handling**: Comprehensive error handling with specific error codes
- **Web UI**: Interactive web interface with example URL tags for quick testing

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
Scrape login elements from a given URL. Automatically tries static scraping first, then falls back to Selenium if no elements are found.

Request body:
```json
{
  "url": "https://example.com/login"
}
```

Response (success):
```json
{
  "success": true,
  "data": {
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
}
```

Response (error):
```json
{
  "success": false,
  "error": {
    "error": "No login elements found on https://example.com/login",
    "error_code": "NO_LOGIN_ELEMENTS"
  }
}
```

**GET /**
Serves the web interface HTML page.

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
2. Enter the URL you want to scrape in the input field or click on one of the example tags
3. Click "Scrape Login Elements"
4. View the results displayed on the page (automatically handles both static and dynamic pages)
5. Copy the JSON results using the "Copy JSON" button

## Output

### CLI Mode
The script will:
1. Fetch the webpage content (static first, then Selenium if needed)
2. Search for login-related input fields using CSS selectors
3. Save found elements to `login_elements.json` (appends to existing data)
4. Display results in the terminal

### API/Web Interface Mode
Returns structured JSON response with login elements found.

## Example CLI Output

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

1. **URL Validation**: Ensures the provided URL is valid and automatically adds https:// if missing
2. **Content Fetching**: Downloads the HTML content
   - Static pages: Uses `requests` library with custom headers
   - Dynamic pages: Uses Selenium with headless Chrome (automatic fallback)
3. **HTML Parsing**: Converts HTML to searchable DOM tree using BeautifulSoup
4. **Element Detection**: Searches for login inputs using comprehensive CSS selectors:
   - Password fields: `input[type="password"]`, `input[autocomplete="current-password"]`
   - Username fields: Various selectors for name, id, email, username attributes
5. **Data Extraction**: Gets the outer HTML of found elements
6. **Storage**: Saves structured data to JSON file (CLI mode) or returns JSON response (API mode)
7. **Error Handling**: Comprehensive exception handling with specific error codes

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

- **Chrome Driver Issues**: Make sure Chrome is installed for Selenium mode (webdriver-manager handles driver installation)
- **Network Errors**: Check your internet connection and URL validity
- **No Elements Found**: The tool automatically tries Selenium if static scraping fails; check if the page actually has login forms
- **API Errors**: Check the response for specific error codes (INVALID_URL, FETCH_ERROR, NO_LOGIN_ELEMENTS, etc.)
- **Port Already in Use**: Make sure port 8000 is available or change the port in the uvicorn command

## Project Structure

```
webscraper-v2/
├── app.py              # FastAPI application with REST endpoints
├── scraper.py          # Core scraping logic and CLI interface
├── index.html          # Web interface HTML
├── script.js           # Frontend JavaScript for web interface
├── styles.css          # CSS styling for web interface
├── requirements.txt    # Python dependencies
├── run.sh              # Shell script to start the server
├── README.md           # This documentation
└── login_elements.json # Output file for CLI mode (created automatically)
```

## License

This project is for educational purposes. Please respect website terms of service and robots.txt files.