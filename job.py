from dataclasses import dataclass

@dataclass
class Job:
    url: str
    title: str
    date_found: str | None = None
    company: str | None = None
    location: str | None = None

    def __str__(self):
        parts = [self.title]
        if self.company:
            parts.append(self.company)
        if self.location:
            parts.append(self.location)
        return f"{' | '.join(parts)}\n  {self.url}"
