from fastapi import FastAPI
from query import fetch_recent_jobs
from filter import filter_jobs
from alert import send_email_alert

app = FastAPI()

# Remove this code from 9-13 after testing

@app.get("/company-list")
def get_company_list(role: str = "data engineer"):
    # TODO: Replace with your dynamic discovery logic
    companies = ["Airbnb", "Stripe", "Netflix", "Snowflake", "Databricks"]
    return companies


#@app.post("/alert")
#def run_alerting():
#    jobs = fetch_recent_jobs()
#    good_jobs = filter_jobs(jobs)
#    send_email_alert(good_jobs)
#    return {"filtered": len(good_jobs)}
#'''
