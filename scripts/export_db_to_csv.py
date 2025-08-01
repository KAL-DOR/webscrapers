import sqlite3
import csv
import time

def export_db_to_csv():
    print("📊 EXPORTING DATABASE JOBS TO CSV")
    print("=" * 40)
    
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    
    # Get all jobs
    cursor.execute('SELECT title, company, location, salary, modality, link, description, source FROM job_listings')
    all_jobs = cursor.fetchall()
    
    print(f"Total jobs in database: {len(all_jobs)}")
    
    # Separate by source
    occ_jobs = []
    computrabajo_jobs = []
    
    for job in all_jobs:
        title, company, location, salary, modality, link, description, source = job
        job_dict = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'modality': modality,
            'link': link,
            'description': description,
            'source': source
        }
        
        if source == 'OCC':
            occ_jobs.append(job_dict)
        elif source == 'Computrabajo':
            computrabajo_jobs.append(job_dict)
    
    print(f"OCC jobs: {len(occ_jobs)}")
    print(f"Computrabajo jobs: {len(computrabajo_jobs)}")
    
    # Export OCC jobs
    if occ_jobs:
        occ_filename = f"db_occ_jobs_{int(time.time())}.csv"
        with open(occ_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in occ_jobs:
                writer.writerow(job)
        print(f"✅ Exported {len(occ_jobs)} OCC jobs to {occ_filename}")
    
    # Export Computrabajo jobs
    if computrabajo_jobs:
        comp_filename = f"db_computrabajo_jobs_{int(time.time())}.csv"
        with open(comp_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for job in computrabajo_jobs:
                writer.writerow(job)
        print(f"✅ Exported {len(computrabajo_jobs)} Computrabajo jobs to {comp_filename}")
    
    # Export all jobs
    all_filename = f"db_all_jobs_{int(time.time())}.csv"
    with open(all_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'company', 'location', 'salary', 'modality', 'link', 'description', 'source']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for job in all_jobs:
            writer.writerow({
                'title': job[0],
                'company': job[1],
                'location': job[2],
                'salary': job[3],
                'modality': job[4],
                'link': job[5],
                'description': job[6],
                'source': job[7]
            })
    print(f"✅ Exported all {len(all_jobs)} jobs to {all_filename}")
    
    conn.close()

if __name__ == "__main__":
    export_db_to_csv() 