# Computrabajo Mexico Job Scraper

A Python package for scraping job listings from Computrabajo Mexico.

## Features

- Scrapes job listings from Computrabajo Mexico
- Extracts job title, company, location, salary, description, and more
- Supports pagination
- Async/await support for better performance
- Error handling and logging

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from ComputrabajoScraper import scrape_jobs_computrabajo

async def main():
    # Scrape jobs for a specific keyword
    jobs = await scrape_jobs_computrabajo("recursos humanos", pages=5)
    
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Salary: {job['salary']}")
        print(f"Link: {job['link']}")
        print("---")

# Run the scraper
asyncio.run(main())
```

## API Reference

### `scrape_jobs_computrabajo(keyword: str, pages: int = 5) -> List[Dict]`

Scrapes job listings from Computrabajo Mexico.

**Parameters:**
- `keyword` (str): Search keyword for jobs
- `pages` (int): Number of pages to scrape (default: 5)

**Returns:**
- `List[Dict]`: List of job dictionaries with the following keys:
  - `title`: Job title
  - `company`: Company name
  - `location`: Job location
  - `salary`: Salary information
  - `description`: Job description
  - `modality`: Work modality (remote, on-site, etc.)
  - `link`: Job application link
  - `source`: Source website (always "Computrabajo")

## License

MIT License 