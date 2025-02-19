import asyncio
import re

from models import init_db, save_jobs_to_db
from scraper import scrape_jobs


async def main():
    await init_db()
    job_searched = input("Ingrese el cargo o categoría:\n").strip().lower()
    job_searched = re.sub(r'\s+', '-', job_searched)
    
    print(f"\n🔍 Buscando vacantes para: {job_searched.replace('-', ' ')}", end="", flush=True)

    
    jobs = await scrape_jobs("desarrollador", pages=5)
    await save_jobs_to_db(jobs)
    print("✅ Trabajos guardados en la base de datos.")


asyncio.run(main())
