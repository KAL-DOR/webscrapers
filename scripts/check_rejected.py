import sqlite3

def is_hr_related_occ(title, description):
    hr_keywords = [
        "recursos humanos", "rrhh", "hr", "human resources", "rh", "capital humano",
        "reclutamiento", "selección", "recruitment", "selection", "reclutador", "reclutadora",
        "talent acquisition", "adquisición de talento", "personal", "capacitación", "training",
        "desarrollo organizacional", "organizational development", "compensaciones", "compensation",
        "beneficios", "benefits", "nómina", "payroll", "relaciones laborales", "labor relations",
        "gestión del talento", "talent management", "analista", "coordinador", "coordinadora",
        "gerente", "director", "directora", "especialista", "consultor", "consultora", "ejecutivo",
        "ejecutiva", "auxiliar", "asistente", "generalista", "onboarding", "inducción", "clima laboral",
        "organizational climate", "evaluación de desempeño", "performance evaluation", "desarrollo de personal",
        "personal development", "administración de personal", "personal administration"
    ]
    title_lower = title.lower()
    description_lower = description.lower()
    return any(keyword in title_lower or keyword in description_lower for keyword in hr_keywords)

def is_mexico_location_occ(location):
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

# Check what's in the database
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

print("=== ANALYZING OCC JOBS ===")

# Get all OCC jobs
cursor.execute('SELECT title, location, description FROM job_listings WHERE source = "OCC"')
occ_jobs = cursor.fetchall()

print(f"Total OCC jobs in DB: {len(occ_jobs)}")

# Analyze locations
locations = {}
for title, location, description in occ_jobs:
    if location not in locations:
        locations[location] = 0
    locations[location] += 1

print(f"\n=== LOCATIONS FOUND ===")
for location, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
    print(f"{location}: {count} jobs")

# Test some sample jobs that might be rejected
print(f"\n=== SAMPLE REJECTION ANALYSIS ===")
sample_jobs = [
    ("Recursos humanos", "CDMX", "Coordinador/a de Recursos Humanos"),
    ("Recursos humanos", "Monterrey,, N.L.", "Ingeniería en Telecomunicaciones"),
    ("RECURSOS HUMANOS", "Álvaro Obregón,, CDMX", "Servicios Administrativos"),
]

for title, location, description in sample_jobs:
    hr_check = is_hr_related_occ(title, description)
    location_check = is_mexico_location_occ(location)
    print(f"Title: {title}")
    print(f"Location: '{location}' -> Location check: {location_check}")
    print(f"HR check: {hr_check}")
    print(f"Would pass: {hr_check and location_check}")
    print("-" * 40)

conn.close() 