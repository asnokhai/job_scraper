import sqlite3


class DBInterface:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_jobs (
                url TEXT PRIMARY KEY,
                title TEXT,
                date_found TEXT,
                company TEXT,
                location TEXT
            )
        """)
        # Migrate existing DBs that are missing the new columns
        existing = {row[1] for row in self.conn.execute("PRAGMA table_info(seen_jobs)")}
        for col, typedef in [("company", "TEXT"), ("location", "TEXT")]:
            if col not in existing:
                self.conn.execute(f"ALTER TABLE seen_jobs ADD COLUMN {col} {typedef}")
        self.conn.commit()

    def get_seen_urls(self):
        rows = self.conn.execute("SELECT url FROM seen_jobs").fetchall()
        return {row[0] for row in rows}

    def save_jobs(self, jobs):
        self.conn.executemany(
            "INSERT OR IGNORE INTO seen_jobs (url, title, date_found, company, location) VALUES (?, ?, ?, ?, ?)",
            [(j.url, j.title, j.date_found, j.company, j.location) for j in jobs],
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()