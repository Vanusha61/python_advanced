"""
В этом файле будут Celery-задачи
"""
from celery import Celery, group
from celery.schedules import crontab


from image import blur_image
from mail import send_newsletter

import redis
r = redis.Redis.from_url('redis://localhost:6379/0', decode_responses=True)

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

@celery.task
def blur_image_task(image_url, filename = None):
    blur_image(image_url,filename)

@celery.task
def send_email_task(email: str, subject: str = "Еженедельная рассылка", message: str = "Привет! Рады видеть тебя среди наших подписчиков. Вот свежие новости..."):
    send_newsletter(email, subject, message)

@celery.task
def send_emails_task():
    emails = r.smembers('email_subscribers')
    if not emails:
        return "No email subscribers found"
    emails = list(emails)
    groups = group(
        send_email_task.s(email) for email in emails
    )
    groups.apply_async()
    return len(emails)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=12, minute=0, day_of_week=7),
        send_emails_task.s(),
    )
