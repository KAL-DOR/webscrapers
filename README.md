# 🇲🇽 Mexico HR Job Scraper

A comprehensive web scraper for HR job listings from Mexican job sites.

## 📁 Project Structure

```
Computrabajo-scrapper/
├── 📁 OCCMexicoScraper/          # OCC Mexico scraper module
│   ├── 📄 scraper_occ.py         # OCC scraper logic
│   ├── 📄 __init__.py            # Package initialization
│   ├── 📄 requirements.txt       # OCC scraper dependencies
│   └── 📄 README.md              # OCC scraper documentation
├── 📁 ComputrabajoScraper/       # Computrabajo scraper module
│   ├── 📄 scraper.py             # Computrabajo scraper logic
│   ├── 📄 main.py                # Computrabajo main script
│   ├── 📄 models.py              # Database models
│   ├── 📄 __init__.py            # Package initialization
│   ├── 📄 requirements.txt       # Computrabajo dependencies
│   └── 📄 README.md              # Computrabajo documentation
├── 📁 exports/                   # CSV exports and data files
├── 📁 scripts/                   # Utility and export scripts
├── 📄 get_3000_occ_jobs_checkpoint.py  # Main checkpoint scraper
├── 📄 get_3000_occ_jobs.py       # Original 3000 jobs scraper
├── 📄 check_checkpoint.py        # Checkpoint status utility
├── 📄 hr_mexico_summary.py       # HR jobs analysis script
├── 📄 jobs.db                    # SQLite database
├── 📄 *.csv                      # Job data exports
└── 📄 requirements.txt           # Main project dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 2. Run Scrapers

**Get 3000+ OCC Jobs (with checkpoint system):**
```bash
python get_3000_occ_jobs_checkpoint.py
```

**Check Progress:**
```bash
python check_checkpoint.py
```

**Get 3000+ OCC Jobs (original):**
```bash
python get_3000_occ_jobs.py
```

**Run Individual Scrapers:**
```bash
# OCC Scraper
python -m OCCMexicoScraper

# Computrabajo Scraper
python -m ComputrabajoScraper
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
- ✅ **Checkpoint System**: Resume from exactly where you left off
- ✅ **Real-time ETA**: Know exactly how long it will take
- ✅ **Real Link Extraction**: Actual job URLs from OCC
- ✅ **Real Description Extraction**: Full job descriptions from job pages
- ✅ **Duplicate Removal**: Smart deduplication by job links
- ✅ **Progress Saving**: Checkpoint saves after each page
- ✅ **Database Integration**: SQLite storage with source tracking
- ✅ **CSV Export**: Direct export to CSV files
- ✅ **Location Filtering**: Mexico-specific location detection
- ✅ **Concurrent Scraping**: Run both scrapers simultaneously

## 📈 Current Status

- **OCC Jobs**: Target 3000+ jobs with real links and descriptions
- **Computrabajo Jobs**: 2500+ jobs
- **Total Database**: 2700+ jobs

## 🔧 Configuration

### OCC Scraper Settings
- **Keywords**: recursos-humanos, rrhh, rh, reclutamiento, seleccion, personal
- **Pages per keyword**: Auto-adjusting (starts at 50)
- **Wait time**: 5-8 seconds between requests
- **Location filter**: Mexico cities and states
- **Real Data**: Extracts actual job URLs and descriptions

### Computrabajo Scraper Settings
- **Keywords**: recursos humanos, rrhh, rh, reclutamiento, seleccion
- **Pages per keyword**: Configurable
- **Wait time**: 2-5 seconds between requests

## 📁 File Organization

### `/OCCMexicoScraper/`
- Complete OCC scraper package
- Real link and description extraction
- Playwright-based browser automation

### `/ComputrabajoScraper/`
- Complete Computrabajo scraper package
- HTTP-based scraping
- Database integration

### `/exports/`
- CSV files with scraped data
- Progress checkpoints
- Final results

### `/scripts/`
- Export utilities
- Database checkers
- Analysis tools

## 🎯 Next Steps

1. **Run Checkpoint Scraper**: `python get_3000_occ_jobs_checkpoint.py`
2. **Check Progress**: `python check_checkpoint.py`
3. **Analyze Data**: Use scripts in `/scripts/` folder
4. **Export Results**: CSV files in `/exports/` folder

## 📞 Support

For issues or questions, check the `/exports/` folder for checkpoint files and progress data.

## 🔄 Recent Updates

- ✅ **Organized Structure**: Separated OCC and Computrabajo scrapers into dedicated folders
- ✅ **Real Data Extraction**: OCC scraper now extracts actual job URLs and descriptions
- ✅ **Package Structure**: Both scrapers are now proper Python packages
- ✅ **Checkpoint System**: Resume scraping from exactly where you left off
- ✅ **Real-time ETA**: Know exactly how long the scraping will take
- ✅ **Page-by-Page Saving**: Never lose progress again
- ✅ **Clean Project**: Removed all test files and unused scripts
