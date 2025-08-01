"""
OCC Mexico Job Scraper Package

This package provides functionality to scrape job listings from OCC.com.mx
"""

from .scraper_occ import scrape_jobs_occ, OCCScraper

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = ["scrape_jobs_occ", "OCCScraper"] 