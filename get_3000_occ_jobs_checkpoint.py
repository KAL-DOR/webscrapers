import asyncio
import csv
import time
import json
import os
from datetime import datetime, timedelta
from OCCMexicoScraper.scraper_occ import scrape_jobs_occ, OCCScraper

# Configuration
TARGET_JOBS = 3000
PAGES_PER_KEYWORD = 50
CHECKPOINT_FILE = "exports/checkpoint.json"
PROGRESS_FILE = "exports/progress.csv"

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

class CheckpointManager:
    def __init__(self, checkpoint_file):
        self.checkpoint_file = checkpoint_file
        self.checkpoint_data = self.load_checkpoint()
    
    def load_checkpoint(self):
        """Load checkpoint data if it exists"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"📂 Loaded checkpoint: {data['total_jobs']} jobs, {data['keywords_completed']} keywords completed")
                    return data
            except Exception as e:
                print(f"⚠️ Error loading checkpoint: {e}")
        
        return {
            'total_jobs': 0,
            'keywords_completed': 0,
            'current_keyword': 0,
            'current_page': 1,
            'seen_links': [],
            'start_time': time.time(),
            'jobs_per_page': [],
            'last_save_time': time.time()
        }
    
    def save_checkpoint(self, all_jobs, keyword_idx, page_num, seen_links, jobs_per_page):
        """Save checkpoint after each page"""
        try:
            checkpoint_data = {
                'total_jobs': len(all_jobs),
                'keywords_completed': keyword_idx - 1,
                'current_keyword': keyword_idx,
                'current_page': page_num,
                'seen_links': list(seen_links),
                'start_time': self.checkpoint_data['start_time'],
                'jobs_per_page': jobs_per_page,
                'last_save_time': time.time()
            }
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.checkpoint_file), exist_ok=True)
            
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving checkpoint: {e}")
    
    def get_progress_stats(self, all_jobs, keyword_idx, page_num):
        """Calculate progress statistics"""
        elapsed = time.time() - self.checkpoint_data['start_time']
        progress = len(all_jobs) / TARGET_JOBS
        
        # Calculate ETA based on current rate
        if elapsed > 0 and len(all_jobs) > 0:
            jobs_per_second = len(all_jobs) / elapsed
            remaining_jobs = TARGET_JOBS - len(all_jobs)
            eta_seconds = remaining_jobs / jobs_per_second if jobs_per_second > 0 else 0
            eta = timedelta(seconds=int(eta_seconds))
        else:
            eta = timedelta(seconds=0)
        
        # Calculate completion percentage
        total_pages = len(hr_keywords) * PAGES_PER_KEYWORD
        completed_pages = (keyword_idx - 1) * PAGES_PER_KEYWORD + page_num
        page_progress = completed_pages / total_pages
        
        return {
            'elapsed': elapsed,
            'progress': progress,
            'eta': eta,
            'page_progress': page_progress,
            'jobs_per_second': jobs_per_second if elapsed > 0 else 0
        }

async def save_to_csv(jobs, filename):
    """Save jobs to CSV file"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in jobs:
                writer.writerow(job)
        return True
    except Exception as e:
        print(f"❌ Error saving to CSV: {str(e)}")
        return False

def format_time(seconds):
    """Format time in HH:MM:SS"""
    return str(timedelta(seconds=int(seconds)))

async def get_3000_occ_jobs_with_checkpoint():
    print("🎯 GETTING 3000+ OCC JOBS WITH CHECKPOINT SYSTEM")
    print("=" * 70)
    print(f"Target: {TARGET_JOBS} unique jobs")
    print(f"Pages per keyword: {PAGES_PER_KEYWORD}")
    print(f"Keywords: {len(hr_keywords)}")
    print(f"Total pages: {len(hr_keywords) * PAGES_PER_KEYWORD}")
    print("=" * 70)
    
    # Initialize checkpoint manager
    checkpoint_manager = CheckpointManager(CHECKPOINT_FILE)
    
    # Load existing data
    all_jobs = []
    seen_links = set(checkpoint_manager.checkpoint_data['seen_links'])
    jobs_per_page = checkpoint_manager.checkpoint_data['jobs_per_page']
    
    # Load existing jobs if checkpoint exists
    if checkpoint_manager.checkpoint_data['total_jobs'] > 0:
        print(f"📂 Resuming from checkpoint: {checkpoint_manager.checkpoint_data['total_jobs']} jobs")
        # Load the latest CSV file
        latest_csv = f"exports/occ_progress_{checkpoint_manager.checkpoint_data['total_jobs']}.csv"
        if os.path.exists(latest_csv):
            try:
                with open(latest_csv, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    all_jobs = list(reader)
                    print(f"📂 Loaded {len(all_jobs)} jobs from {latest_csv}")
            except Exception as e:
                print(f"⚠️ Error loading CSV: {e}")
    
    start_keyword = checkpoint_manager.checkpoint_data['current_keyword']
    if start_keyword == 0:
        start_keyword = 1
    
    print(f"🚀 Starting from keyword {start_keyword}/{len(hr_keywords)}")
    
    for keyword_idx in range(start_keyword, len(hr_keywords) + 1):
        keyword = hr_keywords[keyword_idx - 1]
        print(f"\n🔍 [{keyword_idx}/{len(hr_keywords)}] Scraping keyword: '{keyword}'")
        
        start_page = 1
        if keyword_idx == start_keyword:
            start_page = checkpoint_manager.checkpoint_data['current_page']
        
        for page in range(start_page, PAGES_PER_KEYWORD + 1):
            try:
                print(f"  📄 Page {page}/{PAGES_PER_KEYWORD}...")
                
                # Scrape single page (optimized)
                async with OCCScraper() as scraper:
                    jobs = await scraper.search_jobs_single_page(keyword, page)
                
                # Filter out duplicates
                new_jobs = []
                for job in jobs:
                    if job["link"] not in seen_links and job["link"] != "N/A":
                        seen_links.add(job["link"])
                        new_jobs.append(job)
                
                all_jobs.extend(new_jobs)
                jobs_per_page.append(len(new_jobs))
                
                # Calculate and display progress
                stats = checkpoint_manager.get_progress_stats(all_jobs, keyword_idx, page)
                
                print(f"    ✅ Found {len(jobs)} jobs, {len(new_jobs)} new unique jobs")
                print(f"    📊 Total: {len(all_jobs)}/{TARGET_JOBS} ({stats['progress']*100:.1f}%)")
                print(f"    ⏱️ Elapsed: {format_time(stats['elapsed'])} | ETA: {stats['eta']}")
                print(f"    📈 Rate: {stats['jobs_per_second']:.2f} jobs/sec")
                
                # Save checkpoint after each page
                checkpoint_manager.save_checkpoint(all_jobs, keyword_idx, page, seen_links, jobs_per_page)
                
                # Save to CSV every 100 jobs
                if len(all_jobs) % 100 == 0 and len(all_jobs) > 0:
                    csv_filename = f"exports/occ_progress_{len(all_jobs)}.csv"
                    if await save_to_csv(all_jobs, csv_filename):
                        print(f"    💾 Saved to: {csv_filename}")
                
                # Check if we've reached the target
                if len(all_jobs) >= TARGET_JOBS:
                    print(f"\n🎉 TARGET REACHED! Found {len(all_jobs)} unique jobs")
                    break
                
                # Small delay between pages
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"    ❌ Error on page {page}: {str(e)}")
                continue
        
        if len(all_jobs) >= TARGET_JOBS:
            break
    
    # Final save
    if all_jobs:
        final_csv = "exports/occ_3000_jobs_final.csv"
        if await save_to_csv(all_jobs, final_csv):
            print(f"\n💾 Final results saved to: {final_csv}")
        
        # Save checkpoint
        checkpoint_manager.save_checkpoint(all_jobs, len(hr_keywords) + 1, 1, seen_links, jobs_per_page)
    
    # Final statistics
    total_time = time.time() - checkpoint_manager.checkpoint_data['start_time']
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Total unique jobs: {len(all_jobs)}")
    print(f"Total time: {format_time(total_time)}")
    print(f"Jobs per hour: {len(all_jobs) / (total_time / 3600):.1f}")
    print(f"Average jobs per page: {sum(jobs_per_page) / len(jobs_per_page):.1f}")
    
    if len(all_jobs) >= TARGET_JOBS:
        print("🎯 SUCCESS: Reached target of 3000+ jobs!")
    else:
        print(f"⚠️ WARNING: Only got {len(all_jobs)} jobs, target was {TARGET_JOBS}")
    
    return all_jobs

if __name__ == "__main__":
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)
    
    asyncio.run(get_3000_occ_jobs_with_checkpoint()) 