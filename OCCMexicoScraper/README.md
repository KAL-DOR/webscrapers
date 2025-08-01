# OCC Mexico Job Scraper

A Python package for scraping job listings from OCC.com.mx (OCC Mundial).

## Features

- Asynchronous job scraping with pagination support
- Configurable search keywords and page limits
- Respectful rate limiting between requests
- Comprehensive error handling and logging
- Returns structured job data

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
import asyncio
from OCCMexicoScraper import scrape_jobs_occ

async def main():
    # Scrape jobs for "recursos humanos" keyword
    jobs = await scrape_jobs_occ("recursos humanos", pages=5)
    
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print("---")

asyncio.run(main())
```

### Advanced Usage

```python
from OCCMexicoScraper import OCCScraper

async def custom_scraping():
    async with OCCScraper() as scraper:
        # Custom scraping logic
        jobs = await scraper.search_jobs("desarrollo web", page=1)
        return jobs
```

## Job Data Structure

Each job object contains:

- `title`: Job title
- `company`: Company name
- `location`: Job location
- `description`: Job description/summary
- `salary`: Salary information (if available)
- `url`: Direct link to the job posting
- `source`: Always "OCC"
- `scraped_at`: Timestamp of when the job was scraped

## Configuration

The scraper uses respectful defaults:
- User-Agent: Chrome browser simulation
- Rate limiting: 1-3 seconds between requests
- Base URL: https://www.occ.com.mx

## Error Handling

The scraper includes comprehensive error handling:
- Network request failures
- HTML parsing errors
- Missing data fields
- Rate limiting and blocking detection

## License

This project is for educational purposes. Please respect OCC's terms of service and robots.txt. 