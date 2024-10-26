from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.services import get_posts_from_cache
from .models import Mailing, Message, Client, MailingAttempt
from .forms import MailingForm, MessageForm, ClientForm
from django.urls import reverse_lazy


def home(request):
    total_mailings = Mailing.objects.count()

    active_mailings = Mailing.objects.filter(status='active').count()

    unique_clients = Client.objects.aggregate(count=Count('id', distinct=True))['count']

    all_posts = get_posts_from_cache()
    random_posts = all_posts.order_by('?')[:3]

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'posts': random_posts,
    }
    return render(request, 'home.html', context)


class MailingListView(ListView, LoginRequiredMixin):
    model = Mailing
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.has_perm('mailing_app.view_all_mailings'):
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(DetailView, LoginRequiredMixin):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = MailingAttempt.objects.filter(mailing=self.object).order_by('-attempt_datetime')
        return context


class MailingCreateView(PermissionRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_app:mailing_list')
    permission_required = 'mailing_app.can_edit_mailing'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing_app:mailing_list')
    permission_required = 'mailing_app.can_edit_mailing'

    def dispatch(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        if mailing.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на редактирование данной рассылки.")
        return super().dispatch(request, *args, **kwargs)


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing_app:mailing_list')
    permission_required = 'mailing_app.can_edit_mailing'

    def dispatch(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        if mailing.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на удаление данной рассылки.")
        return super().dispatch(request, *args, **kwargs)


class MessageListView(ListView, LoginRequiredMixin):
    model = Message
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView, LoginRequiredMixin):
    model = Message


class MessageCreateView(PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_app:message_list')
    permission_required = 'mailing_app.can_edit_message'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing_app:message_list')
    permission_required = 'mailing_app.can_edit_message'

    def dispatch(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=self.kwargs['pk'])
        if message.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на редактирование данного сообщения.")
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing_app:message_list')
    permission_required = 'mailing_app.can_edit_message'

    def dispatch(self, request, *args, **kwargs):
        message = get_object_or_404(Message, pk=self.kwargs['pk'])
        if message.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на удаление данного сообщения.")
        return super().dispatch(request, *args, **kwargs)


class ClientListView(ListView, LoginRequiredMixin):
    model = Client
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_app:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_app:client_list')

    def dispatch(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        if client.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на редактирование данного клиента.")
        return super().dispatch(request, *args, **kwargs)


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy('mailing_app:client_list')

    def dispatch(self, request, *args, **kwargs):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        if client.owner != request.user:
            return HttpResponseForbidden("У вас нет прав на удаление данного клиента.")
        return super().dispatch(request, *args, **kwargs)
