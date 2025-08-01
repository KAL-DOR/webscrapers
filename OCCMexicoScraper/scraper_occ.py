import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCCScraper:
    def __init__(self):
        self.base_url = "https://www.occ.com.mx"
        self.playwright = None
        self.browser = None
        self.page = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def search_jobs(self, keyword: str, page: int = 1) -> List[Dict]:
        """Search for jobs on OCC with pagination"""
        try:
            # Construct search URL with correct pagination structure
            search_url = f"{self.base_url}/empleos/de-{keyword}/"
            if page > 1:
                search_url += f"?page={page}"
            
            logger.info(f"Searching: {search_url}")
            
            # Navigate to the page
            await self.page.goto(search_url, timeout=60000)
            await self.page.wait_for_timeout(3000)
            
            # Scroll to load all content
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(2000)
            
            # Get the HTML content
            html = await self.page.content()
            return await self.parse_jobs_page(html)
                
        except Exception as e:
            logger.error(f"Error searching jobs on page {page}: {e}")
            return []
    
    async def get_job_description(self, job_url: str) -> str:
        """Get job description by visiting the job page"""
        try:
            # Navigate to the job page
            await self.page.goto(job_url, timeout=30000)
            await self.page.wait_for_timeout(2000)
            
            # Get the HTML content
            html = await self.page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for description elements - OCC specific selectors based on real HTML
            description_elem = (
                soup.find('div', class_='break-words mb-8') or  # Main description container
                soup.find('div', class_='[&>p]:m-0 [&>p]:p-0 [&>img]:w-[100vh] [&>img]:h-auto overflow-hidden [&>ul]:list-disc [&>ul]:list-inside font-light [&>p]:font-normal [&>ul>li>strong]:font-bold [&>ul]:indent-5') or  # Description content
                soup.find('div', class_='job-description') or
                soup.find('div', class_='description') or
                soup.find('div', class_='job-details') or
                soup.find('div', class_='content') or
                soup.find('div', class_='body') or
                soup.find('p', class_='description') or
                soup.find('div', {'data-testid': 'job-description'}) or
                soup.find('div', class_='job-content') or
                soup.find('div', class_='job-summary') or
                soup.find('div', class_='job-requirements') or
                soup.find('div', class_='job-responsibilities') or
                soup.find('div', class_='job-duties') or
                soup.find('section', class_='job-description') or
                soup.find('article', class_='job-description')
            )
            
            if description_elem:
                # Clean up the text
                text = description_elem.get_text(strip=True)
                # Remove extra whitespace and newlines
                text = ' '.join(text.split())
                return text
            else:
                # Try to find description by looking for "Descripción" text
                desc_heading = soup.find('p', string=lambda text: text and 'Descripción' in text)
                if desc_heading:
                    # Get the next sibling div that contains the description
                    next_div = desc_heading.find_next_sibling('div')
                    if next_div:
                        text = next_div.get_text(strip=True)
                        text = ' '.join(text.split())
                        return text
                
                # Try to find any text content that might be the description
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='main')
                if main_content:
                    text = main_content.get_text(strip=True)
                    text = ' '.join(text.split())
                    if len(text) > 100:  # Only return if it's substantial
                        return text
                
                return "Descripción no disponible"
                
        except Exception as e:
            logger.error(f"Error getting description from {job_url}: {e}")
            return "Error al obtener descripción"
    
    async def parse_jobs_page(self, html: str) -> List[Dict]:
        """Parse job listings from HTML page"""
        jobs = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find job cards using OCC's structure (div with id starting with "jobcard-")
        job_cards = soup.select('div[id^="jobcard-"]')
        
        logger.info(f"Found {len(job_cards)} job cards on page")
        
        for card in job_cards:
            try:
                job = await self.extract_job_data(card)
                if job:
                    jobs.append(job)
            except Exception as e:
                logger.error(f"Error parsing job card: {e}")
                continue
        
        return jobs
    
    async def extract_job_data(self, card) -> Optional[Dict]:
        """Extract job data from a job card element"""
        try:
            # Extract job ID from the card's id attribute
            job_id = card.get('id', '').replace('jobcard-', '')
            
            # Extract title - try multiple approaches
            title = "N/A"
            title_elem = (
                card.find('h2') or 
                card.find('h3') or 
                card.find('h4') or
                card.find('a', class_='job-title') or
                card.find('a', class_='title') or
                card.find('a', href=True)  # Often the title is in a link
            )
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            # Extract company - based on the actual HTML structure
            company = "N/A"
            # Look for the div that contains both company and location
            company_location_div = card.find('div', class_='flex flex-row justify-between items-center')
            if company_location_div:
                # Get all text and split by location
                full_text = company_location_div.get_text(strip=True)
                # Company is usually the first part before the comma
                if ',' in full_text:
                    company = full_text.split(',')[0].strip()
                else:
                    company = full_text
            else:
                # Fallback to other selectors
                company_elem = (
                    card.find('span', class_='company') or 
                    card.find('div', class_='company-name') or
                    card.find('a', class_='company-link') or
                    card.find('span', class_='employer') or
                    card.find('span', class_='company-name') or
                    card.find('div', class_='employer') or
                    card.find('p', class_='company')
                )
                if company_elem:
                    company = company_elem.get_text(strip=True)
            
            # Extract location - based on the actual HTML structure
            location = "N/A"
            # Look for the div that contains both company and location
            company_location_div = card.find('div', class_='flex flex-row justify-between items-center')
            if company_location_div:
                # Get all text and split by location
                full_text = company_location_div.get_text(strip=True)
                # Location is usually the part after the comma
                if ',' in full_text:
                    location = full_text.split(',', 1)[1].strip()
                else:
                    location = full_text
            else:
                # Fallback to other selectors
                location_elem = (
                    card.find('span', class_='location') or 
                    card.find('div', class_='job-location') or
                    card.find('span', class_='city') or
                    card.find('p', class_='location') or
                    card.find('span', class_='job-location') or
                    card.find('div', class_='location') or
                    card.find('span', class_='place')
                )
                if location_elem:
                    location = location_elem.get_text(strip=True)
            
            # Extract description/summary - try multiple approaches
            description = "N/A"
            desc_elem = (
                card.find('p', class_='description') or 
                card.find('div', class_='job-summary') or
                card.find('div', class_='job-description') or
                card.find('p', class_='summary') or
                card.find('div', class_='description') or
                card.find('p', class_='job-description') or
                card.find('span', class_='description')
            )
            if desc_elem:
                description = desc_elem.get_text(strip=True)
            
            # Extract salary - based on the actual HTML structure
            salary = "N/A"
            # Look for the salary span with specific classes
            salary_elem = card.find('span', class_='mr-2 text-grey-900 font-base font-light mb-4')
            if salary_elem:
                salary = salary_elem.get_text(strip=True)
            else:
                # Fallback to other selectors
                salary_elem = (
                    card.find('span', class_='salary') or 
                    card.find('div', class_='job-salary') or
                    card.find('span', class_='compensation') or
                    card.find('span', class_='pay') or
                    card.find('div', class_='salary') or
                    card.find('p', class_='salary')
                )
                if salary_elem:
                    salary = salary_elem.get_text(strip=True)
            
            # Extract job URL using the job ID from the card
            job_url = "N/A"
            job_id = card.get('id', '').replace('jobcard-', '')
            if job_id:
                job_url = f"{self.base_url}/empleos/empleo-{job_id}/"
            

            
            # Extract description by visiting the job page
            description = "N/A"
            if job_url != "N/A":
                try:
                    description = await self.get_job_description(job_url)
                except Exception as e:
                    logger.error(f"Error getting description for {job_url}: {e}")
                    description = "Error al obtener descripción"
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'salary': salary,
                'modality': 'N/A',  # OCC doesn't always show modality
                'link': job_url,
                'source': 'OCC'
            }
            
        except Exception as e:
            logger.error(f"Error extracting job data: {e}")
            return None

async def scrape_jobs_occ(keyword: str, pages: int = 5) -> List[Dict]:
    """
    Main function to scrape jobs from OCC
    
    Args:
        keyword (str): Search keyword for jobs
        pages (int): Number of pages to scrape
    
    Returns:
        List[Dict]: List of job dictionaries
    """
    all_jobs = []
    
    async with OCCScraper() as scraper:
        for page in range(1, pages + 1):
            logger.info(f"Scraping page {page}/{pages} for keyword: {keyword}")
            
            jobs = await scraper.search_jobs(keyword, page)
            
            # Process each job to get descriptions
            processed_jobs = []
            for i, job in enumerate(jobs):
                logger.info(f"Processing job {i+1}/{len(jobs)} on page {page}")
                processed_jobs.append(job)
                
                # Add small delay between job processing
                if i < len(jobs) - 1:
                    await asyncio.sleep(random.uniform(0.5, 1))
            
            all_jobs.extend(processed_jobs)
            
            logger.info(f"Found {len(jobs)} jobs on page {page}")
            
            # Add delay between pages to be respectful
            if page < pages:
                delay = random.uniform(2, 4)
                await asyncio.sleep(delay)
    
    logger.info(f"Total jobs scraped: {len(all_jobs)}")
    return all_jobs

# For testing
if __name__ == "__main__":
    async def test_scraper():
        jobs = await scrape_jobs_occ("recursos humanos", pages=2)
        print(f"Scraped {len(jobs)} jobs")
        for job in jobs[:3]:  # Show first 3 jobs
            print(f"- {job['title']} at {job['company']}")
    
    asyncio.run(test_scraper()) 