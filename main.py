from motorsports_jobs_scraper import MotorsportsJobsScraper
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
]


def main():
    scraper = MotorsportsJobsScraper(KEYWORDS)

    with DBInterface(DB_PATH) as db:
        seen_urls = db.get_seen_urls()
        all_jobs = scraper.get_all_jobs()

        new_jobs = [j for j in all_jobs if j.url not in seen_urls]

        if not new_jobs:
            print("\nNo new jobs since last run.")
        else:
            print(f"\n{'='*60}")
            print(f"  {len(new_jobs)} NEW JOB(S) FOUND")
            print(f"{'='*60}\n")
            for job in new_jobs:
                print(f"  {job.title}")
                print(f"  {job.url}")
                print()
            db.save_jobs(new_jobs)


if __name__ == "__main__":
    main()