from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import scraper  # Import the existing scraper module

app = FastAPI(title="Web Scraper API", description="API for scraping login elements from web pages")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (but exclude API routes)
app.mount("/static", StaticFiles(directory=".", html=False), name="static")

# Data models using dataclasses (no pydantic dependency)
from dataclasses import dataclass

@dataclass
class ScrapeRequest:
    url: str

@dataclass
class LoginElement:
    type: str
    html: str

@dataclass
class ScrapeResponse:
    url: str
    login_elements: List[LoginElement]
    count: int

@dataclass
class ErrorResponse:
    success: bool = False
    error: str = ""
    error_code: str = ""
    details: Optional[str] = None

@dataclass
class APIResponse:
    success: bool
    data: Optional[ScrapeResponse] = None
    error: Optional[ErrorResponse] = None

@app.post("/scrape", response_model=APIResponse)
async def scrape_login_elements(request: ScrapeRequest):
    """
    Scrape login elements from a given URL.

    Args:
        request: ScrapeRequest containing URL

    Returns:
        APIResponse with success data or error details
    """
    try:
        # Validate URL using existing function
        request.url = scraper.validate_url(request.url)

        # Fetch page content - start with static
        html_content = scraper.fetch_page_content(request.url, False)

        # Parse HTML
        soup = scraper.parse_html(html_content)

        # Find login elements
        login_elements_raw = scraper.find_login_elements(soup)

        # If no login elements found with static scraping, try with Selenium
        if not login_elements_raw:
            html_content = scraper.fetch_page_content(request.url, True)
            soup = scraper.parse_html(html_content)
            login_elements_raw = scraper.find_login_elements(soup)

        # Convert to Pydantic models
        login_elements = [
            LoginElement(type=element['type'], html=element['html'])
            for element in login_elements_raw
        ]

        response_data = ScrapeResponse(
            url=request.url,
            login_elements=login_elements,
            count=len(login_elements)
        )

        return APIResponse(success=True, data=response_data)

    except scraper.InvalidURLError as e:
        return APIResponse(
            success=False,
            error=ErrorResponse(
                error=str(e),
                error_code=e.error_code
            )
        )
    except scraper.FetchError as e:
        return APIResponse(
            success=False,
            error=ErrorResponse(
                error=str(e),
                error_code=e.error_code
            )
        )
    except scraper.ParseError as e:
        return APIResponse(
            success=False,
            error=ErrorResponse(
                error=str(e),
                error_code=e.error_code
            )
        )
    except scraper.NoLoginElementsError as e:
        return APIResponse(
            success=False,
            error=ErrorResponse(
                error=str(e),
                error_code=e.error_code
            )
        )
    except Exception as e:
        return APIResponse(
            success=False,
            error=ErrorResponse(
                error="An unexpected error occurred",
                error_code="UNKNOWN_ERROR",
                details=str(e)
            )
        )

@app.get("/")
async def root():
    return FileResponse("index.html", media_type="text/html")