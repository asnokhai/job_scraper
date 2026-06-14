import httpx
from bs4 import BeautifulSoup
from datetime import date
from db_interface import DBInterface

# --- Config ---
DB_PATH = "jobs.db"
SITEMAP_URL = "https://www.motorsportjobs.com/en/sitemap.xml"
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
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
}


# --- Sitemap ---
def fetch_all_job_urls():
    r = httpx.get(SITEMAP_URL, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "xml")
    urls = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
    job_urls = [u for u in urls if "/en/job/" in u]
    print(f"  Sitemap: {len(job_urls)} job URLs found")
    return job_urls


# --- Keyword filter ---
def title_matches(url):
    slug = url.rstrip("/").split("/")[-1]
    slug_lower = slug.lower().replace("-", " ")
    return any(kw.lower() in slug_lower for kw in KEYWORDS)


# --- Main ---
def main():
    with DBInterface(DB_PATH) as db:
        seen_urls = db.get_seen_urls()
        all_job_urls = fetch_all_job_urls()

        matched = [u for u in all_job_urls if title_matches(u)]
        print(f"  Keyword matches: {len(matched)}")

        new_jobs = [
            {"url": u, "title": u.rstrip("/").split("/")[-1].replace("-", " ").title(), "date_found": str(date.today())}
            for u in matched if u not in seen_urls
        ]

        if not new_jobs:
            print("\nNo new jobs since last run.")
        else:
            print(f"\n{'='*60}")
            print(f"  {len(new_jobs)} NEW JOB(S) FOUND")
            print(f"{'='*60}\n")
            for job in new_jobs:
                print(f"  {job['title']}")
                print(f"  {job['url']}")
                print()
            db.save_jobs(new_jobs)


if __name__ == "__main__":
    main()