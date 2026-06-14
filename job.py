from dataclasses import dataclass

@dataclass
class Job:
    url: str
    title: str
    date_found: str | None = None
    company: str | None = None
    location: str | None = None
