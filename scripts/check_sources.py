import sqlite3

conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

# Count by source
cursor.execute('SELECT source, COUNT(*) FROM job_listings GROUP BY source')
results = cursor.fetchall()
print("=== JOBS BY SOURCE ===")
for source, count in results:
    print(f"{source}: {count} jobs")

print("\n=== FIRST 5 OCC JOBS ===")
cursor.execute('SELECT title, company, location FROM job_listings WHERE source = "OCC" LIMIT 5')
occ_jobs = cursor.fetchall()
for title, company, location in occ_jobs:
    print(f"{title} | {company} | {location}")

print("\n=== FIRST 5 COMPUTRABAJO JOBS ===")
cursor.execute('SELECT title, company, location FROM job_listings WHERE source = "Computrabajo" LIMIT 5')
comp_jobs = cursor.fetchall()
for title, company, location in comp_jobs:
    print(f"{title} | {company} | {location}")

conn.close() 