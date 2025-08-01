import sqlite3
import pandas as pd
from collections import Counter

def hr_mexico_summary():
    conn = sqlite3.connect('jobs.db')
    
    print("🇲🇽 RESUMEN DE VACANTES DE RECURSOS HUMANOS EN MÉXICO")
    print("=" * 60)
    
    # Get all jobs
    df = pd.read_sql_query("SELECT * FROM job_listings", conn)
    
    print(f"📊 Total de vacantes encontradas: {len(df)}")
    
    # Top locations
    print(f"\n📍 Top 10 Ubicaciones:")
    location_counts = df['location'].value_counts().head(10)
    for i, (location, count) in enumerate(location_counts.items(), 1):
        print(f"{i:2d}. {location}: {count} vacantes")
    
    # Top companies
    print(f"\n🏢 Top 10 Empresas:")
    company_counts = df['company'].value_counts().head(10)
    for i, (company, count) in enumerate(company_counts.items(), 1):
        print(f"{i:2d}. {company}: {count} vacantes")
    
    # Salary analysis
    print(f"\n💰 Análisis de Salarios:")
    salary_df = df[df['salary'] != 'No especificado']
    if len(salary_df) > 0:
        print(f"Vacantes con salario especificado: {len(salary_df)}")
        
        # Extract numeric values from salary strings
        salaries = []
        for salary in salary_df['salary']:
            try:
                # Extract numbers from salary strings like "$ 8,400.00 (Mensual)"
                import re
                numbers = re.findall(r'[\d,]+', salary)
                if numbers:
                    # Remove commas and convert to float
                    clean_number = float(numbers[0].replace(',', ''))
                    salaries.append(clean_number)
            except:
                continue
        
        if salaries:
            print(f"Salario promedio: ${sum(salaries)/len(salaries):,.2f} MXN")
            print(f"Salario mínimo: ${min(salaries):,.2f} MXN")
            print(f"Salario máximo: ${max(salaries):,.2f} MXN")
    else:
        print("No hay información de salarios disponible")
    
    # Job title analysis
    print(f"\n💼 Tipos de Puestos más Comunes:")
    title_counts = df['title'].value_counts().head(10)
    for i, (title, count) in enumerate(title_counts.items(), 1):
        print(f"{i:2d}. {title}: {count} vacantes")
    
    # Modality analysis
    print(f"\n🏠 Modalidad de Trabajo:")
    modality_counts = df['modality'].value_counts()
    for modality, count in modality_counts.items():
        print(f"• {modality}: {count} vacantes")
    
    conn.close()

if __name__ == "__main__":
    hr_mexico_summary() 