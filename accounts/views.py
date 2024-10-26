from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .forms import UserRegistrationForm
from .models import CustomUser
from .services import send_verification_email


@permission_required('accounts.view_customuser', raise_exception=True)
def accounts_list(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/account_list.html', {'accounts': users})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            users_group = Group.objects.get(name='Users')
            user.groups.add(users_group)

            send_verification_email(request, user)
            messages.success(request, 'Регистрация прошла успешно. Проверьте вашу почту для подтверждения.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

