import httpx
import json
import numpy as np
from datetime import date
from job import Job

API_URL = "https://porsche-beesite-production-gjb.app.beesite.de/search/"
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Origin": "https://jobs.porsche.com",
    "Referer": "https://jobs.porsche.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}
COUNT_PER_PAGE = 20


class PorscheScraper:
    def __init__(self, keywords):
        self.keywords = keywords

    def _build_payload(self, first_item: int, count: int) -> dict:
        return {
            "SearchParameters": {
                "FirstItem": first_item,
                "CountItem": count,
                "MatchedObjectDescriptor": [
                    "PositionTitle",
                    "PositionLocation.CityName",
                    "PositionLocation.CountryName",
                    "PositionURI",
                ],
            },
            "SearchCriteria": [
                {"CriterionName": "PublicationChannel.Code", "CriterionValue": ["12"]}
            ],
            "LanguageCode": "EN",
        }

    def _fetch_page(self, first_item: int) -> dict:
        payload = self._build_payload(first_item, COUNT_PER_PAGE)
        r = httpx.get(
            API_URL,
            params={"data": json.dumps(payload)},
            headers=HEADERS,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def _matches_keywords(self, title: str) -> bool:
        title_lower = title.lower()
        return any(kw.lower() in title_lower for kw in self.keywords)

    def get_all_jobs(self) -> np.ndarray:
        # First request to get total count
        first_page = self._fetch_page(1)
        total = first_page["SearchResult"]["SearchResultCountAll"]
        print(f"  Total Porsche jobs: {total}")

        all_items = first_page["SearchResult"]["SearchResultItems"]

        # Paginate through the rest
        for first_item in range(COUNT_PER_PAGE + 1, total + 1, COUNT_PER_PAGE):
            page = self._fetch_page(first_item)
            all_items.extend(page["SearchResult"]["SearchResultItems"])

        print(f"  Fetched {len(all_items)} jobs")

        jobs = []
        for item in all_items:
            desc = item["MatchedObjectDescriptor"]
            title = desc.get("PositionTitle")

            if not title or not self._matches_keywords(title):
                continue

            url = desc.get("PositionURI")
            locations = desc.get("PositionLocation", [])
            location = locations[0]["CityName"] if locations else None

            jobs.append(Job(
                url=url,
                title=title,
                company="Porsche",
                location=location,
                date_found=str(date.today()),
            ))

        print(f"  Keyword matches: {len(jobs)}")
        return np.array(jobs)

if __name__ == "__main__":
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

    porsche_scraper = PorscheScraper(KEYWORDS)

    for job in porsche_scraper.get_all_jobs():
        print(job)