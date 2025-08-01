import httpx
from bs4 import BeautifulSoup
import asyncio
import random
import time
from models import save_jobs_to_db

BASE_URL = "https://mx.computrabajo.com"


async def scrape_jobs(keyword, pages=60, location_filter="México"):
    print(f"[DEBUG] Starting scrape_jobs for {keyword}, {pages} pages")
    # Header necesario para simular que la petición la hace un navegador web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    jobs = []
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        for page in range(1, pages + 1):
            url = f"{BASE_URL}/trabajo-de-{keyword}?p={page}"
            try:
                response = await client.get(url, headers=headers, timeout=30.0)
                if response.status_code != 200:
                    print(f"Error al obtener la página {page}: Status {response.status_code}")
                    continue
            except Exception as e:
                print(f"Error al obtener la página {page}: {str(e)}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article", class_="box_offer")

            # Throttle between page requests
            await asyncio.sleep(random.uniform(1, 4))

            page_jobs = []
            for article in articles:
                title_tag = article.find("a", class_="js-o-link fc_base")
                
                # Improved company extraction with multiple selectors
                company_tag = None
                company_selectors = [
                    article.find("a", attrs={"offer-grid-article-company-url": ""}),
                    article.find("a", class_="fc_base"),
                    article.find("span", class_="fs16"),
                    article.find("p", class_="fs16"),
                    article.find("div", class_="fs16")
                ]
                
                for selector in company_selectors:
                    if selector and selector != title_tag:
                        company_tag = selector
                        break
                
                location_tag = article.find("p", class_="fs16 fc_base mt5")
                salary_tag = article.find("span", class_="icon i_salary")
                modality_tag = article.find("span", class_="icon i_home_office")

                # Obtener la URL real de la oferta
                job_url = BASE_URL + title_tag["href"] if title_tag else None
                clean_job_url = job_url.replace("\t", "/t") if job_url else None

                # Obtener la descripción (segunda petición)
                description = "No disponible"
                if clean_job_url:
                    try:
                        desc_response = await client.get(clean_job_url, headers=headers, timeout=30.0)
                        if desc_response.status_code == 200:
                            desc_soup = BeautifulSoup(desc_response.text, "html.parser")
                            desc_div = desc_soup.find(
                                "p", class_="mbB"
                            )  # Se ajusta de acuerdo al contenedor que tiene la información de la vacante, en este momento es el p con la clase mbB
                            if not desc_div:
                                desc_div = desc_soup.find(
                                    "div", {"id": "job-description"}
                                )  # Alternativa

                            description = (
                                desc_div.text.strip() if desc_div else "No disponible"
                            )
                    except Exception as e:
                        description = "Error al obtener descripción"
                    # Throttle between job detail requests
                    await asyncio.sleep(random.uniform(1, 2))

                job = {
                    "title": title_tag.text.strip() if title_tag else "No especificado",
                    "company": (
                        company_tag.text.strip() if company_tag else "No especificado"
                    ),
                    "location": (
                        location_tag.text.strip() if location_tag else "No especificado"
                    ),
                    "salary": (
                        salary_tag.next_sibling.strip()
                        if salary_tag
                        else "No especificado"
                    ),
                    "modality": (
                        modality_tag.next_sibling.strip()
                        if modality_tag
                        else "No especificado"
                    ),
                    "link": job_url if job_url else "No disponible",
                    "description": description,
                    "source": "Computrabajo",
                }
                
                # Since we're already searching for HR keywords, we only need to filter by Mexico location
                # and do a basic HR check to ensure relevance
                if is_mexico_location(job["location"]) and is_hr_related(job["title"], job["description"]):
                    page_jobs.append(job)
            jobs.extend(page_jobs)
            # Save progress after each page
            if page_jobs:
                await save_jobs_to_db(page_jobs)
                for job in page_jobs:
                    print(f"{job['title']} | {job['company']} | {job['location']} | {job['salary']}")
            # ETA calculation
            elapsed = time.time() - start_time
            avg_per_page = elapsed / page
            pages_left = pages - page
            eta = int(avg_per_page * pages_left)
            eta_min, eta_sec = divmod(eta, 60)
            print(f"[Progress] Keyword: {keyword}, Page {page}/{pages}, Jobs so far: {len(jobs)}, ETA: {eta_min:02d}:{eta_sec:02d}")

    return jobs


def is_hr_related(title, description):
    """Check if the job is related to Human Resources (more flexible)"""
    hr_keywords = [
        # Core HR terms
        "recursos humanos", "rrhh", "hr", "human resources", 
        "rh", "capital humano", "human capital",
        
        # Recruitment and selection
        "reclutamiento", "selección", "recruitment", "selection",
        "reclutador", "reclutadora", "seleccionador", "seleccionadora",
        "talent acquisition", "adquisición de talento",
        
        # HR functions
        "personal", "capacitación", "training", "desarrollo organizacional", 
        "organizational development", "compensaciones", "compensation", 
        "beneficios", "benefits", "nómina", "payroll", "relaciones laborales", 
        "labor relations", "gestión del talento", "talent management",
        
        # HR roles
        "analista", "coordinador", "coordinadora", "gerente", "director", 
        "directora", "especialista", "consultor", "consultora", "ejecutivo", 
        "ejecutiva", "auxiliar", "asistente", "generalista",
        
        # Specific HR terms
        "onboarding", "inducción", "clima laboral", "organizational climate",
        "evaluación de desempeño", "performance evaluation", "desarrollo de personal",
        "personal development", "administración de personal", "personal administration"
    ]
    
    title_lower = title.lower()
    description_lower = description.lower()
    
    # Check if any HR keyword is in title or description
    return any(keyword in title_lower or keyword in description_lower for keyword in hr_keywords)


def is_mexico_location(location):
    """Check if the location is in Mexico"""
    mexico_keywords = [
        "méxico", "mexico", "cdmx", "ciudad de méxico", "guadalajara", "monterrey",
        "puebla", "tijuana", "mérida", "merida", "querétaro", "queretaro", "juárez",
        "juarez", "leon", "león", "toluca", "chihuahua", "morelia", "hermosillo", 
        "saltillo", "aguascalientes", "zacatecas", "san luis potosí", "san luis potosi", 
        "durango", "colima", "manzanillo", "acapulco", "cancún", "cancun", "puerto vallarta", 
        "oaxaca", "tuxtla gutiérrez", "tuxtla gutierrez", "villahermosa", "campeche", 
        "chetumal", "cozumel", "playa del carmen", "ensenada", "la paz", "los cabos", 
        "mazatlán", "mazatlan", "culiacán", "culiacan", "nuevo laredo", "matamoros", 
        "reynosa", "ciudad victoria", "tampico", "veracruz", "xalapa", "tuxtla", 
        "chiapas", "tabasco", "yucatán", "yucatan", "quintana roo", "baja california", 
        "baja california sur", "sonora", "coahuila", "nuevo león", "nuevo leon", 
        "tamaulipas", "sinaloa", "jalisco", "michoacán", "michoacan", "guerrero", 
        "morelos", "tlaxcala", "hidalgo", "guanajuato", "palenque", "benito juárez",
        "miguel hidalgo", "cuauhtémoc", "iztapalapa", "tlalpan", "coyoacán", "coyoacan",
        "alvaro obregón", "alvaro obregon", "magdalena contreras", "milpa alta", 
        "tlahuac", "xochimilco", "venustiano carranza", "gustavo a. madero", "azcapotzalco"
    ]
    
    location_lower = location.lower()
    return any(keyword in location_lower for keyword in mexico_keywords)
