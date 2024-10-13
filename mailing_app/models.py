from django.db import models


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    PERIODICITY_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    start_datetime = models.DateTimeField()
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)

    def __str__(self):
        return f"Рассылка #{self.id} - {self.message.subject}"


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
