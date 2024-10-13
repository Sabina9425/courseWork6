# mailing_app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .mailing_utils import send_mailing


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        send_mailing,
        'interval',
        minutes=1,
        name='send_mailing',
        jobstore='default',
        replace_existing=True,
    )

    scheduler.start()
