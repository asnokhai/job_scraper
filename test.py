import httpx
import json

API_URL = "https://porsche-beesite-production-gjb.app.beesite.de/search/"

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Origin": "https://jobs.porsche.com",
    "Referer": "https://jobs.porsche.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}

payload = {
    "SearchParameters": {
        "FirstItem": 1,
        "CountItem": 20,
        "MatchedObjectDescriptor": [
            "PositionTitle",
            "PositionLocation.CityName",
            "PositionLocation.CountryName",
            "PositionURI",
            "OrganizationShortName",
        ]
    },
    "SearchCriteria": [
        {"CriterionName": "PublicationChannel.Code", "CriterionValue": ["12"]}
    ],
    "LanguageCode": "EN"
}

r = httpx.get(API_URL, params={"data": json.dumps(payload)}, headers=HEADERS, timeout=30)
print(r.status_code)
print(r.text[:3000])