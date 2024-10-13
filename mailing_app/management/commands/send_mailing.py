from django.core.management.base import BaseCommand
from mailing_app.mailing_utils import send_mailing


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_mailing()
        self.stdout.write(self.style.SUCCESS('Рассылки отправлены'))
