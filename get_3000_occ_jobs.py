import asyncio
import csv
import time
from OCCMexicoScraper.scraper_occ import scrape_jobs_occ

# Configuration
TARGET_JOBS = 3000
PAGES_PER_KEYWORD = 50  # Increased to get more jobs per keyword
SAVE_INTERVAL = 500  # Save progress every 500 jobs

hr_keywords = [
    "recursos-humanos",
    "rrhh",
    "rh",
    "reclutamiento",
    "seleccion",
    "personal",
    "talent-acquisition",
    "human-resources",
    "recruitment",
    "generalista-de-recursos-humanos",
    "analista-de-recursos-humanos",
    "coordinador-de-recursos-humanos",
    "jefe-de-recursos-humanos",
    "lider-de-recursos-humanos",
    "especialista-de-recursos-humanos",
    "becario-de-recursos-humanos",
    "practicante-de-recursos-humanos",
    "auxiliar-de-recursos-humanos",
    "asistente-de-recursos-humanos",
    "gerente-de-recursos-humanos"
]

async def get_3000_occ_jobs():
    print("🎯 GETTING 3000+ OCC JOBS WITH URL PAGINATION")
    print("=" * 60)
    print(f"Target: {TARGET_JOBS} unique jobs")
    print(f"Pages per keyword: {PAGES_PER_KEYWORD}")
    print(f"Keywords: {len(hr_keywords)}")
    print(f"Estimated total pages: {len(hr_keywords) * PAGES_PER_KEYWORD}")
    print("=" * 60)
    
    all_jobs = []
    seen_links = set()  # For in-memory deduplication
    start_time = time.time()
    
    for keyword_idx, keyword in enumerate(hr_keywords, 1):
        print(f"\n🔍 [{keyword_idx}/{len(hr_keywords)}] Scraping keyword: '{keyword}'")
        
        try:
            # Scrape jobs for this keyword
            jobs = await scrape_jobs_occ(keyword, pages=PAGES_PER_KEYWORD)
            
            # Filter out duplicates in memory
            new_jobs = []
            for job in jobs:
                if job["link"] not in seen_links and job["link"] != "No disponible":
                    seen_links.add(job["link"])
                    new_jobs.append(job)
            
            all_jobs.extend(new_jobs)
            
            print(f"✅ Found {len(jobs)} jobs, {len(new_jobs)} new unique jobs")
            print(f"📊 Total unique jobs so far: {len(all_jobs)}")
            
            # Calculate progress and ETA
            elapsed = time.time() - start_time
            progress = len(all_jobs) / TARGET_JOBS
            if progress > 0:
                eta_total = elapsed / progress
                eta_remaining = eta_total - elapsed
                eta_min, eta_sec = divmod(int(eta_remaining), 60)
                eta_hour, eta_min = divmod(eta_min, 60)
                print(f"⏱️ Progress: {progress*100:.1f}% | ETA: {eta_hour:02d}:{eta_min:02d}:{eta_sec:02d}")
            
            # Save progress periodically
            if len(all_jobs) % SAVE_INTERVAL == 0 and len(all_jobs) > 0:
                await save_to_csv(all_jobs, f"exports/occ_progress_{len(all_jobs)}.csv")
                print(f"💾 Progress saved: {len(all_jobs)} jobs")
            
            # Check if we've reached the target
            if len(all_jobs) >= TARGET_JOBS:
                print(f"\n🎉 TARGET REACHED! Found {len(all_jobs)} unique jobs")
                break
                
        except Exception as e:
            print(f"❌ Error with keyword '{keyword}': {str(e)}")
            continue
    
    # Final save
    if all_jobs:
        await save_to_csv(all_jobs, "exports/occ_3000_jobs.csv")
        print(f"\n💾 Final results saved to: exports/occ_3000_jobs.csv")
    
    # Final statistics
    total_time = time.time() - start_time
    hours, remainder = divmod(total_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Total unique jobs: {len(all_jobs)}")
    print(f"Total time: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
    print(f"Jobs per hour: {len(all_jobs) / (total_time / 3600):.1f}")
    
    if len(all_jobs) >= TARGET_JOBS:
        print("🎯 SUCCESS: Reached target of 3000+ jobs!")
    else:
        print(f"⚠️ WARNING: Only got {len(all_jobs)} jobs, target was {TARGET_JOBS}")
    
    return all_jobs

async def save_to_csv(jobs, filename):
    """Save jobs to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in jobs:
                writer.writerow(job)
    except Exception as e:
        print(f"❌ Error saving to CSV: {str(e)}")

if __name__ == "__main__":
    # Create exports directory if it doesn't exist
    import os
    os.makedirs("exports", exist_ok=True)
    
    asyncio.run(get_3000_occ_jobs()) 