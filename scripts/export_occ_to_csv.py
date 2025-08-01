import asyncio
import csv
import time
from OCCMexicoScraper.scraper_occ import scrape_jobs_occ

async def export_occ_to_csv():
    print("🇲🇽 EXPORTING OCC JOBS TO CSV")
    print("=" * 50)
    
    # Test with just the first keyword for now
    hr_keywords = [
        "recursos-humanos",
        # "rrhh",
        # "rh", 
        # "reclutamiento",
        # "seleccion",
        # "personal",
    ]
    
    all_jobs = []
    
    for keyword in hr_keywords:
        print(f"\n🔍 Scraping keyword: {keyword}")
        jobs = await scrape_jobs_occ(keyword, pages=5)  # Just 5 pages for testing
        all_jobs.extend(jobs)
        print(f"✅ Found {len(jobs)} jobs for keyword '{keyword}'")
    
    print(f"\n📊 Total jobs found: {len(all_jobs)}")
    
    # Export to CSV
    csv_filename = f"occ_jobs_{int(time.time())}.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for job in all_jobs:
            writer.writerow(job)
    
    print(f"✅ Exported {len(all_jobs)} jobs to {csv_filename}")
    
    # Show first 5 jobs
    print(f"\n📋 First 5 jobs:")
    for i, job in enumerate(all_jobs[:5], 1):
        print(f"\n--- Job {i} ---")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Salary: {job['salary']}")
        print(f"Link: {job['link']}")

if __name__ == "__main__":
    asyncio.run(export_occ_to_csv()) 