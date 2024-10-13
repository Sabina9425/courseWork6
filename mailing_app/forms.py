from django import forms
from .models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_datetime', 'periodicity', 'status', 'message', 'clients']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
