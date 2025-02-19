import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://co.computrabajo.com"


async def scrape_jobs(keyword, pages=1):
    # Header necesario para simular que la petición la hace un navegador web
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    jobs = []

    async with httpx.AsyncClient() as client:
        for page in range(1, pages + 1):
            url = f"{BASE_URL}/trabajo-de-{keyword}?p={page}"
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error al obtener la página {page}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article", class_="box_offer")

            for article in articles:
                title_tag = article.find("a", class_="js-o-link fc_base")
                company_tag = article.find(
                    "a", attrs={"offer-grid-article-company-url": ""}
                )
                location_tag = article.find("p", class_="fs16 fc_base mt5")
                salary_tag = article.find("span", class_="icon i_salary")
                modality_tag = article.find("span", class_="icon i_home_office")

                # Obtener la URL real de la oferta
                job_url = BASE_URL + title_tag["href"] if title_tag else None
                clean_job_url = job_url.replace("\t", "/t")

                # Obtener la descripción (segunda petición)
                description = "No disponible"
                if clean_job_url:
                    desc_response = await client.get(clean_job_url, headers=headers)
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
                }
                jobs.append(job)

    return jobs
