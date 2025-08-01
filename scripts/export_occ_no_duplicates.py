import asyncio
import csv
import time
from OCCMexicoScraper.scraper_occ import scrape_jobs_occ

async def export_occ_no_duplicates():
    print("🇲🇽 EXPORTING OCC JOBS TO CSV (NO DUPLICATES)")
    print("=" * 50)
    
    # All keywords
    hr_keywords = [
        "recursos-humanos",
        "rrhh",
        "rh", 
        "reclutamiento",
        "seleccion",
        "personal",
    ]
    
    all_jobs = []
    seen_links = set()  # To track duplicates
    
    for keyword in hr_keywords:
        print(f"\n🔍 Scraping keyword: {keyword}")
        jobs = await scrape_jobs_occ(keyword, pages=10)  # 10 pages per keyword
        
        # Remove duplicates
        unique_jobs = []
        for job in jobs:
            if job['link'] not in seen_links:
                seen_links.add(job['link'])
                unique_jobs.append(job)
        
        all_jobs.extend(unique_jobs)
        print(f"✅ Found {len(jobs)} jobs, {len(unique_jobs)} unique for keyword '{keyword}'")
    
    print(f"\n📊 Total unique jobs found: {len(all_jobs)}")
    
    # Export to CSV
    csv_filename = f"occ_jobs_unique_{int(time.time())}.csv"
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for job in all_jobs:
            writer.writerow(job)
    
    print(f"✅ Exported {len(all_jobs)} unique jobs to {csv_filename}")
    
    # Show summary
    print(f"\n📋 Summary:")
    print(f"Total unique jobs: {len(all_jobs)}")
    print(f"CSV file: {csv_filename}")
    
    # Show first 3 jobs as sample
    print(f"\n📋 Sample jobs:")
    for i, job in enumerate(all_jobs[:3], 1):
        print(f"\n--- Job {i} ---")
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Salary: {job['salary']}")

if __name__ == "__main__":
    asyncio.run(export_occ_no_duplicates()) 