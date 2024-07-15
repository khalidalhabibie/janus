from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import send_scheduled_emails
from datetime import datetime, timedelta


def start_scheduler(app):
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(send_scheduled_emails, 'interval', minutes=1, args=[app])
    print(f"Scheduled a one-time job with ID: {job.id} to run at", datetime.now() + timedelta(minutes=1))
    scheduler.start()
