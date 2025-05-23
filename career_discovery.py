from fastapi import FastAPI
from pydantic import BaseModel
from serpapi import GoogleSearch
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4
from datetime import datetime
import os

app = FastAPI()

# Define request format
class CompanyInput(BaseModel):
    companies: list

# Connect to Astra DB
def get_session():
    cloud_config = {'secure_connect_bundle': './secure-connect-your-db'}
    auth_provider = PlainTextAuthProvider(
        os.getenv("ASTRA_DB_CLIENT_ID"),
        os.getenv("ASTRA_DB_CLIENT_SECRET")
    )
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster.connect(os.getenv("ASTRA_DB_KEYSPACE"))

session = get_session()

@app.post("/discover-career-pages")
def discover_pages(data: CompanyInput):
    discovered = []
    for company in data.companies:
        query = f"site:{company.lower()}.com careers OR jobs"
        search = GoogleSearch({
            "q": query,
            "api_key": os.getenv("SERPAPI_KEY"),
            "num": 3
        })
        results = search.get_dict()
        career_url = None
        for result in results.get("organic_results", []):
            link = result.get("link", "")
            if any(word in link.lower() for word in ["careers", "jobs", "join", "work-at"]):
                career_url = link
                break

        if career_url:
            session.execute("""
                INSERT INTO job_postings (id, title, company, location, url, source, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                uuid4(),
                "Company Careers",
                company,
                "United States",
                career_url,
                "scraped-career-page",
                datetime.utcnow()
            ))
            discovered.append({company: career_url})

    return {"found": discovered}
