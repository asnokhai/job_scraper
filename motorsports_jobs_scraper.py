from job import Job
import numpy as np
import httpx
from bs4 import BeautifulSoup
from datetime import date

SITEMAP_URL = "https://www.motorsportjobs.com/en/sitemap.xml"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
}


class MotorsportsJobsScraper:
    def __init__(self, keywords):
        self.keywords = keywords

    def get_all_jobs(self) -> np.ndarray:
        r = httpx.get(SITEMAP_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "xml")
        urls = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
        job_urls = [u for u in urls if "/en/job/" in u]
        print(f"  Sitemap: {len(job_urls)} job URLs found")

        matched = [u for u in job_urls if self._matches_keywords(u)]
        print(f"  Keyword matches: {len(matched)}")

        jobs = [self._url_to_job(u) for u in matched]
        return np.array(jobs)

    def _matches_keywords(self, url: str) -> bool:
        slug = url.rstrip("/").split("/")[-1].lower().replace("-", " ")
        return any(kw.lower() in slug for kw in self.keywords)

    def _url_to_job(self, url: str) -> Job:
        slug = url.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ").title()
        return Job(url=url, title=title, date_found=str(date.today()))