from fastapi import FastAPI
from query import fetch_recent_jobs
from filter import filter_jobs
from alert import send_email_alert

app = FastAPI()


@app.post("/alert")
def run_alerting():
    jobs = fetch_recent_jobs()
    good_jobs = filter_jobs(jobs)
    send_email_alert(good_jobs)
    return {"filtered": len(good_jobs)}

