# 🇲🇽 Mexico HR Job Scraper

A comprehensive web scraper for HR job listings from Mexican job sites.

## 📁 Project Structure

```
Computrabajo-scrapper/
├── 📁 OCCMexicoScraper/          # OCC Mexico scraper module
├── 📁 exports/                   # CSV exports and data files
├── 📁 scripts/                   # Utility and export scripts
├── 📁 temp/                      # Temporary files and tests
├── 📄 main.py                    # Computrabajo scraper main script
├── 📄 scraper.py                 # Computrabajo scraper logic
├── 📄 models.py                  # Database models
├── 📄 jobs.db                    # SQLite database
├── 📄 get_3000_occ_jobs.py      # Get 3000+ OCC jobs script
└── 📄 requirements.txt           # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 2. Run Scrapers

**Get 3000+ OCC Jobs:**
```bash
python get_3000_occ_jobs.py
```

**Run Computrabajo Scraper:**
```bash
python main.py
```

**Run OCC Scraper (Full):**
```bash
python -m OCCMexicoScraper
```

### 3. Export Data

**Export Database to CSV:**
```bash
python scripts/export_db_to_csv.py
```

**Export OCC Jobs (No Duplicates):**
```bash
python scripts/export_occ_no_duplicates.py
```

## 📊 Data Sources

- **OCC Mexico**: HR job listings from occ.com.mx
- **Computrabajo**: HR job listings from mx.computrabajo.com

## 🎯 Features

- ✅ **3000+ OCC Jobs**: Automatic scraping until target reached
- ✅ **Duplicate Removal**: Smart deduplication by job links
- ✅ **Progress Saving**: Checkpoint saves every 500 jobs
- ✅ **Database Integration**: SQLite storage with source tracking
- ✅ **CSV Export**: Direct export to CSV files
- ✅ **ETA Display**: Real-time progress with time estimates
- ✅ **Location Filtering**: Mexico-specific location detection

## 📈 Current Status

- **OCC Jobs**: Target 3000+ jobs
- **Computrabajo Jobs**: 2500+ jobs
- **Total Database**: 2700+ jobs

## 🔧 Configuration

### OCC Scraper Settings
- **Keywords**: recursos-humanos, rrhh, rh, reclutamiento, seleccion, personal
- **Pages per keyword**: Auto-adjusting (starts at 50)
- **Wait time**: 5-8 seconds between requests
- **Location filter**: Mexico cities and states

### Computrabajo Scraper Settings
- **Keywords**: recursos humanos, rrhh, rh, reclutamiento, seleccion
- **Pages per keyword**: Configurable
- **Wait time**: 2-5 seconds between requests

## 📁 File Organization

### `/exports/`
- CSV files with scraped data
- Progress checkpoints
- Final results

### `/scripts/`
- Export utilities
- Database checkers
- Analysis tools

### `/temp/`
- Test files
- Debug HTML files
- Temporary data

## 🎯 Next Steps

1. **Run 3000 OCC Jobs**: `python get_3000_occ_jobs.py`
2. **Check Progress**: Monitor exports folder
3. **Analyze Data**: Use scripts in `/scripts/` folder
4. **Export Results**: CSV files in `/exports/` folder

## 📞 Support

For issues or questions, check the `/temp/` folder for debug files and test results.
