import sqlite3
import json
import time
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

app = Flask(__name__, static_folder="static")
CORS(app)

DB_PATH = "jobs.db"
GEO_CACHE_PATH = "geocache.json"

geolocator = Nominatim(user_agent="job_map_app_v2")


def load_geocache():
    try:
        with open(GEO_CACHE_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_geocache(cache):
    with open(GEO_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def geocode(location, cache):
    if not location:
        return None, None
    key = location.strip()
    if key in cache:
        return cache[key].get("lat"), cache[key].get("lng")
    try:
        time.sleep(1.1)
        result = geolocator.geocode(key, timeout=10)
        if result:
            cache[key] = {"lat": result.latitude, "lng": result.longitude}
            save_geocache(cache)
            return result.latitude, result.longitude
    except (GeocoderTimedOut, GeocoderServiceError):
        pass
    cache[key] = {"lat": None, "lng": None}
    save_geocache(cache)
    return None, None


@app.route("/api/jobs")
def get_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT url, title, company, location, date_found FROM seen_jobs"
    ).fetchall()
    conn.close()

    cache = load_geocache()
    jobs = []

    for row in rows:
        lat, lng = geocode(row["location"], cache)
        if lat and lng:
            jobs.append({
                "url": row["url"],
                "title": row["title"],
                "company": row["company"] or "Unknown",
                "location": row["location"] or "Unknown",
                "date_found": row["date_found"],
                "lat": lat,
                "lng": lng,
            })

    return jsonify(jobs)


@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/debug")
def debug():
    import os
    return {
        "cwd": os.getcwd(),
        "static_folder": app.static_folder,
        "index_exists": os.path.exists(os.path.join(app.static_folder, "index.html"))
    }

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    print("Starting Job Map at http://localhost:8080")
    app.run(debug=False, port=8080)