import numpy as np

from scrapers.motorsports_jobs_scraper import MotorsportsJobsScraper
from scrapers.porsche_scraper import PorscheScraper
from db_interface import DBInterface

DB_PATH = "jobs.db"
KEYWORDS = [
    "simulation",
    "simulator",
    "vehicle dynamics",
    "motion platform",
    "motion cueing",
    "driving simulator",
    "hexapod",
    "washout",
    "HIL",
    "motion system",
    "junior"
]

scrapers = [
    MotorsportsJobsScraper(KEYWORDS),
    PorscheScraper(KEYWORDS),
]

with DBInterface(DB_PATH) as db:
    seen_urls = db.get_seen_urls()

    results = []
    for scraper in scrapers:
        try:
            results.append(scraper.get_all_jobs())
        except Exception as e:
            print(f"[ERROR] {scraper.__class__.__name__} failed: {e}")

    all_jobs = np.concatenate(results) if results else np.array([])
    new_jobs = [j for j in all_jobs if j.url not in seen_urls]

    if not new_jobs:
        print("\nNo new jobs since last run.")
    else:
        print(f"\n{'='*60}")
        print(f"  {len(new_jobs)} NEW JOB(S) FOUND")
        print(f"{'='*60}\n")
        for job in new_jobs:
            print(job)
        db.save_jobs(new_jobs)

