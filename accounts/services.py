from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import CustomUser


def send_verification_email(request, user):
    subject = 'Подтверждение регистрации'
    email_template_name = 'accounts/verification_email.html'
    context = {
        'user': user,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string(email_template_name, context)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        login(request, user)
        messages.success(request, 'Ваш аккаунт успешно активирован.')
        return redirect('mailing_app:mailing_list')
    else:
        messages.error(request, 'Ссылка активации недействительна.')
        return redirect('login')


@permission_required('accounts.change_customuser', raise_exception=True)
def block_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f'Пользователь {user.username} заблокирован.')
        return redirect('accounts')
    return render(request, 'accounts/block_account_confirm.html', {'user': user})


@permission_required('accounts.change_customuser', raise_exception=True)
def unlock_account(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        messages.success(request, f'Пользователь {user.username} разблокирован.')
        return redirect('accounts')
    return render(request, 'accounts/unlock_account_confirm.html', {'user': user})