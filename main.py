from fastapi import FastAPI
from fastapi.responses import JSONResponse
from query import fetch_recent_jobs
from filter import filter_jobs
from alert import send_email_alert
import traceback

app = FastAPI()

@app.post("/alert")
def run_alerting():
    try:
        jobs = fetch_recent_jobs()
        good_jobs = filter_jobs(jobs)
        send_email_alert(good_jobs)
        return {"filtered": len(good_jobs)}
    except Exception:
        print("Exception during alerting:")
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"error": "Something went wrong while running alerts"}
        )
