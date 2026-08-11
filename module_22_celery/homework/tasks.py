"""
В этом файле будут Celery-задачи
"""
from celery import Celery, group
from celery.schedules import crontab

from image import blur_image
from mail import send_newsletter

import redis

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
import os

r = redis.Redis.from_url('redis://localhost:6379/0', decode_responses=True)

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)


@celery.task
def blur_image_task(image_url, filename=None):
    res = blur_image(image_url, filename)
    return res


@celery.task
def send_email_task(email: str, subject: str = "Еженедельная рассылка",
                    message: str = "Привет! Рады видеть тебя среди наших подписчиков. Вот свежие новости..."):
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


@celery.task
def send_result_task(results, email):
    """Отправляет одно письмо на почту `email` со всеми обработанными файлами из списка `results`."""
    msg = MIMEMultipart()
    msg['Subject'] = 'Ваши обработанные изображения'
    msg['From'] = SMTP_USER
    msg['To'] = email

    # Можно добавить текстовое сопровождение
    msg.attach(MIMEText('Готовые размытые изображения во вложении.'))

    for file_path in results:
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(file_path)}'
        )
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, email, msg.as_string())

    return f"Email sent to {email} with {len(results)} attachments"