from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm
from .models import CustomUser
from .services import send_verification_email


@permission_required('accounts.view_customuser', raise_exception=True)
def accounts_list(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/account_list.html', {'accounts': users})


class CustomUserDetailView(DetailView, LoginRequiredMixin):
    model = CustomUser


class CustomUserEditView(UpdateView, LoginRequiredMixin):
    model = CustomUser
    fields = ("first_name", "last_name")
    template_name = "accounts/customuser_edit.html"

    def get_success_url(self):
        return reverse('user_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        user = self.request.user

        if user.is_authenticated:
            return user
        else:
            raise PermissionDenied


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

