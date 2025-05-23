from fastapi import FastAPI
from pydantic import BaseModel
import requests
from uuid import uuid4
from datetime import datetime
import os

app = FastAPI()

# ENV: Set these securely on Render
ASTRA_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_TOKEN = os.getenv("ASTRA_DB_API_TOKEN")
ASTRA_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

class CompanyInput(BaseModel):
    companies: list

@app.post("/discover-careers")
def discover_pages(data: CompanyInput):
    discovered = []

    for company in data.companies:
        query = f"site:{company.lower()}.com careers OR jobs"
        serp_resp = requests.get("https://serpapi.com/search", params={
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "num": 3
        })

        results = serp_resp.json()
        url = None
        for result in results.get("organic_results", []):
            link = result.get("link", "")
            if any(word in link.lower() for word in ["careers", "jobs", "join", "work-at"]):
                url = link
                break

        if url:
            job_doc = {
                "id": str(uuid4()),
                "title": "Company Careers",
                "company": company,
                "location": "United States",
                "url": url,
                "source": "scraped-career-page",
                "timestamp": datetime.utcnow().isoformat()
            }

            headers = {
                "X-Cassandra-Token": ASTRA_TOKEN,
                "Content-Type": "application/json"
            }

            endpoint = f"{ASTRA_ENDPOINT}/api/rest/v2/keyspaces/{ASTRA_KEYSPACE}/job_postings"
            res = requests.post(endpoint, headers=headers, json=job_doc)
            if res.status_code == 201:
                discovered.append({company: url})

    return {"career_pages_found": discovered}
