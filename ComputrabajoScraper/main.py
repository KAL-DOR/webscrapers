import asyncio
import re
import os

from models import init_db, save_jobs_to_db
from scraper import scrape_jobs


async def main():
    # Clear existing database to start fresh
    if os.path.exists("jobs.db"):
        os.remove("jobs.db")
        print("🗑️ Base de datos anterior eliminada.")
    
    await init_db()
    
    print("🇲🇽 SCRAPER DE VACANTES DE RECURSOS HUMANOS EN MÉXICO")
    print("=" * 60)
    
    # Focus on the most effective HR keywords that will capture more positions
    hr_keywords = [
        "recursos-humanos",  # Main HR term
        "rrhh",              # Abbreviation
        "rh",                # Short form
        "reclutamiento",     # Recruitment
        "seleccion",         # Selection
        "personal",          # Personnel
    ]
    
    all_jobs = []
    
    for keyword in hr_keywords:
        print(f"\n🔍 Buscando vacantes para: {keyword.replace('-', ' ')}")
        # Search many more pages to capture more results
        jobs = await scrape_jobs(keyword, pages=25)  # Increased from 10 to 25 pages
        all_jobs.extend(jobs)
        print(f"✅ Encontradas {len(jobs)} vacantes de {keyword}")
    
    # Remove duplicates based on link
    unique_jobs = []
    seen_links = set()
    for job in all_jobs:
        if job["link"] not in seen_links:
            unique_jobs.append(job)
            seen_links.add(job["link"])
    
    print(f"\n📊 Total de vacantes únicas encontradas: {len(unique_jobs)}")
    
    if unique_jobs:
        await save_jobs_to_db(unique_jobs)
        print("✅ Trabajos guardados en la base de datos.")
        
        # Show some statistics
        locations = [job["location"] for job in unique_jobs]
        mexico_city_jobs = [loc for loc in locations if "ciudad de méxico" in loc.lower() or "cdmx" in loc.lower()]
        print(f"📍 Vacantes en Ciudad de México: {len(mexico_city_jobs)}")
        
        # Company statistics
        companies = [job["company"] for job in unique_jobs if job["company"] != "No especificado"]
        unique_companies = len(set(companies))
        print(f"🏢 Empresas únicas: {unique_companies}")
        
    else:
        print("❌ No se encontraron vacantes que cumplan los criterios.")


asyncio.run(main())
