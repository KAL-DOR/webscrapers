#!/usr/bin/env python3
"""
Check checkpoint status and progress
"""

import json
import os
import csv
from datetime import datetime

CHECKPOINT_FILE = "exports/checkpoint.json"

def check_checkpoint():
    """Check the current checkpoint status"""
    print("📊 CHECKPOINT STATUS")
    print("=" * 50)
    
    if not os.path.exists(CHECKPOINT_FILE):
        print("❌ No checkpoint file found")
        print("   Run: python get_3000_occ_jobs_checkpoint.py")
        return
    
    try:
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📂 Checkpoint loaded: {data['total_jobs']} jobs")
        print(f"🔍 Keywords completed: {data['keywords_completed']}")
        print(f"📍 Current keyword: {data['current_keyword']}")
        print(f"📄 Current page: {data['current_page']}")
        
        # Calculate progress
        target_jobs = 3000
        progress = (data['total_jobs'] / target_jobs) * 100
        
        print(f"📈 Progress: {data['total_jobs']}/{target_jobs} ({progress:.1f}%)")
        
        # Show timing info
        if 'start_time' in data:
            elapsed = datetime.now().timestamp() - data['start_time']
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            print(f"⏱️ Elapsed time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Show jobs per page stats
        if 'jobs_per_page' in data and data['jobs_per_page']:
            avg_jobs = sum(data['jobs_per_page']) / len(data['jobs_per_page'])
            print(f"📊 Average jobs per page: {avg_jobs:.1f}")
        
        # Check for CSV files
        csv_files = []
        if os.path.exists("exports"):
            for file in os.listdir("exports"):
                if file.startswith("occ_progress_") and file.endswith(".csv"):
                    csv_files.append(file)
        
        if csv_files:
            csv_files.sort()
            latest_csv = csv_files[-1]
            print(f"💾 Latest CSV: {latest_csv}")
            
            # Count jobs in latest CSV
            try:
                with open(f"exports/{latest_csv}", 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    job_count = sum(1 for row in reader)
                    print(f"📋 Jobs in latest CSV: {job_count}")
            except Exception as e:
                print(f"⚠️ Error reading CSV: {e}")
        
        print("\n🚀 To resume scraping:")
        print("   python get_3000_occ_jobs_checkpoint.py")
        
    except Exception as e:
        print(f"❌ Error reading checkpoint: {e}")

if __name__ == "__main__":
    check_checkpoint() 