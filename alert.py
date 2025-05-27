import os
import smtplib
from email.mime.text import MIMEText

def send_email_alert(jobs):
    if not jobs:
        return

    content = "\n\n".join([f"{job.title} at {job.company} - {job.url}" for job in jobs])
    msg = MIMEText(content)
    msg["Subject"] = "New Data Engineer Jobs 🧠"
    msg["From"] = os.getenv("ALERT_EMAIL_FROM")
    msg["To"] = os.getenv("ALERT_EMAIL_TO")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("ALERT_EMAIL_FROM"), os.getenv("ALERT_EMAIL_PASS"))
        server.send_message(msg)
