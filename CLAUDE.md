# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Scrape new jobs and save them to jobs.db
python main.py

# Start the web map UI (http://localhost:8080)
python app.py

# Run an individual scraper for quick testing
python scrapers/porsche_scraper.py

# Probe an API or HTML structure
python test.py
```

## Architecture

The project has two distinct modes of operation:

**Scraping pipeline** (`main.py`): Instantiates one or more scraper classes, collects `Job` objects, deduplicates against `jobs.db` via `DBInterface`, and prints/saves only the new ones. Run this periodically to keep the database fresh.

**Web UI** (`app.py`): A Flask server that reads `jobs.db`, geocodes each job location via Nominatim (with results persisted to `geocache.json` to avoid repeated API calls), and exposes `/api/jobs` as JSON. The single-page frontend (`static/index.html`) renders jobs on a Leaflet map with a filterable sidebar.

### Data model

`Job` (in `job.py`) is a dataclass with `url`, `title`, `date_found`, `company`, and `location`. URL is the primary key in `seen_jobs` (SQLite via `DBInterface`).

### Adding a new scraper

Each scraper lives in `scrapers/` and must implement `get_all_jobs() -> np.ndarray` returning an array of `Job` objects. Keyword filtering is done inside the scraper — the constructor receives the `KEYWORDS` list from `main.py`. Register the new scraper in `main.py` alongside the existing ones and concatenate its output into `all_jobs`.

### Geocoding

`app.py` geocodes lazily on each `/api/jobs` request and caches results in `geocache.json`. Jobs without a resolvable location are silently excluded from the map response. The 1.1 s sleep between Nominatim calls is required to comply with the usage policy.

### Key constraints

- `MotorsportsJobsScraper` matches keywords against the URL slug, not the page title — keep keywords hyphenable.
- `PorscheScraper` uses a private Beesite JSON API; the payload structure (`SearchParameters`, `SearchCriteria`) must match what the endpoint expects.
- `bmw_scraper.py` is exploratory/scratch code — it is not wired into `main.py` and contains hardcoded session cookies that expire.
