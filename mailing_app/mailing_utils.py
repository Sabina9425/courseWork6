import smtplib

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt


def send_mailing():
    current_datetime = timezone.now()

    mailings = Mailing.objects.filter(
        start_datetime__lte=current_datetime,
        status__in=['created', 'started']
    )

    for mailing in mailings:
        last_attempt = MailingAttempt.objects.filter(mailing=mailing).order_by('-attempt_datetime').first()
        should_send = False

        if not last_attempt:
            should_send = True
        else:
            time_since_last_attempt = current_datetime - last_attempt.attempt_datetime

            if mailing.periodicity == 'daily' and time_since_last_attempt.days >= 1:
                should_send = True
            elif mailing.periodicity == 'weekly' and time_since_last_attempt.days >= 7:
                should_send = True
            elif mailing.periodicity == 'monthly' and time_since_last_attempt.days >= 30:
                should_send = True

        if should_send:
            mailing.status = 'started'
            mailing.save()

            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='success',
                        server_response='Email sent successfully.'
                    )
                except smtplib.SMTPException as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='failed',
                        server_response=str(e)
                    )

            if mailing.periodicity == 'once':
                mailing.status = 'finished'
                mailing.save()


@permission_required('mailing_app.can_disable_mailing', raise_exception=True)
def disable_mailing(request, pk):
    mailing = get_object_or_404(Mailing, id=pk)
    if request.method == 'POST':
        mailing.status = 'disabled'
        mailing.save()
        return redirect('mailing_app:mailing_list')
    return render(request, 'mailing_app/disable_mailing_confirm.html', {'mailing': mailing})


@permission_required('mailing_app.can_disable_mailing', raise_exception=True)
def enable_mailing(request, pk):
    mailing = get_object_or_404(Mailing, id=pk)
    if request.method == 'POST':
        mailing.status = 'created'
        mailing.save()
        return redirect('mailing_app:mailing_list')
    return render(request, 'mailing_app/enable_mailing_confirm.html', {'mailing': mailing})
