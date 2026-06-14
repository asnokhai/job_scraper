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

    def _get_all_job_urls(self):
        r = httpx.get(SITEMAP_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "xml")
        urls = [loc.get_text(strip=True) for loc in soup.find_all("loc")]
        job_urls = [u for u in urls if "/en/job/" in u]

        print(f"  Sitemap: {len(job_urls)} job URLs found")

        return job_urls


    def get_all_jobs(self) -> np.ndarray:
        job_urls = self._get_all_job_urls()
        matched_urls = [url for url in job_urls if self._matches_keywords(url)]
        print(f"  Keyword matches: {len(matched_urls)}")

        jobs = []
        for url in matched_urls:
            job = self._fetch_job_details(url)
            jobs.append(job)

        return np.array(jobs)

    def _matches_keywords(self, url: str) -> bool:
        slug = url.rstrip("/").split("/")[-1].lower().replace("-", " ")
        return any(kw.lower() in slug for kw in self.keywords)

    def _fetch_job_details(self, url: str) -> Job:
        try:
            r = httpx.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            title_el = soup.select_one(".pane-node-title h1, .pane-node-title h2")
            title = title_el.get_text(strip=True) if title_el else None

            company_el = soup.select_one(".pane-node-recruiter-company-profile-job-organization")
            if company_el:
                inner = company_el.select_one("a")
                company = inner.get_text(strip=True) if inner else company_el.get_text(strip=True)
            else:
                company = None

            location_el = soup.select_one(".pane-node-field-job-region span:not(.recruiter-epiq-icon)")
            location = location_el.get_text(strip=True) if location_el else None

        except httpx.HTTPError as e:
            print(f"  [ERROR] {url}: {e}")
            title, company, location = None, None, None

        return Job(url=url, title=title, company=company, location=location, date_found=str(date.today()))