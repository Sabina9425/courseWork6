from time import sleep

from django.apps import AppConfig
import threading


class MailingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing_app'

    def ready(self):
        from .scheduler import start
        sleep(2)
        threading.Thread(target=start).start()
