from django.db import models
from django.conf import settings


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.subject

    class Meta:
        permissions = [
            ('can_edit_message', "Can Edit Message")
        ]


class Mailing(models.Model):
    PERIODICITY_CHOICES = [
        ('once', 'Один раз'),
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
        ('disabled', 'Выключена'),
    ]

    start_datetime = models.DateTimeField()
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Рассылка #{self.id} - {self.message.subject}"

    class Meta:
        permissions = [
            ('can_disable_mailing', "Can Disable Mailing"),
            ('view_all_mailings', "Can View All Mailings"),
            ('can_edit_mailing', "Can Edit Mailing"),
        ]


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Неуспешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Попытка #{self.id} для рассылки #{self.mailing.id}"

    class Meta:
        get_latest_by = 'attempt_datetime'
